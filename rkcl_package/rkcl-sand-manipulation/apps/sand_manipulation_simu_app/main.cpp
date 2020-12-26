#include <rkcl/robots/bazar.h>
#include <rkcl/drivers/vrep_driver.h>
#include <rkcl/processors/otg_reflexxes.h>
#include <rkcl/processors/app_utility.h>
#include <rkcl/processors/internal/internal_functions.h>
#include <yaml-cpp/yaml.h>
#include <pid/rpath.h>
#include <pid/signal_manager.h>

int main()
{
    // Declare the drivers used in the app so that their are known by the program
    rkcl::DriverFactory::add<rkcl::VREPMainDriver>("vrep_main");
    rkcl::DriverFactory::add<rkcl::VREPJointDriver>("vrep_joint");

    //Same for the QP solver used by the controller
    rkcl::QPSolverFactory::add<rkcl::OSQPSolver>("osqp");

    // Load the main configuration file which parametrizes the app
    auto conf_app = YAML::LoadFile(PID_PATH("app_config/sand_manipulation_simu_init_config.yaml"));
    // Create an app utility object. It manages the creation, configuration and call to the different processes in the controller as well as the comminication with the drivers
    auto app = rkcl::AppUtility::create<rkcl::ForwardKinematicsRBDyn, rkcl::JointSpaceOTGReflexxes>(conf_app);

    // Load the names of different actions to perform by the robot, from the config file
    auto actions = conf_app["app"]["actions"].as<std::vector<std::string>>();

    // Load the workspace calibration file. When using the real robot, the parameters it contains can be obtained by launching the 'workspace_calibration' app
    // Here (on simulation) we define the parameters using the VREP scene
    auto conf_ws_calibration = YAML::LoadFile(PID_PATH("app_config/workspace_calibration_simu_data.yaml"));
    // Transformation from world frame to the origin of the sand area (bottom left corner from Bazar point of view)
    Eigen::Affine3d world_T_sand;
    Eigen::Vector3d position(conf_ws_calibration["reference_position"].as<std::vector<double>>().data());
    Eigen::Quaterniond quat(conf_ws_calibration["reference_quaternion"].as<std::vector<double>>().data());
    world_T_sand.translation() = position;
    world_T_sand.linear() = quat.matrix();
    // Dimension of the workspace (dx, dy)
    auto dim_ws = conf_ws_calibration["dimension"].as<std::array<double, 2>>();

    // Rotation matrix from the sand frame to the hand's control point when the operation are performed
    Eigen::Matrix3d sand_R_hand;
    sand_R_hand << -1, 0, 0,
        0, 0, 1,
        0, 1, 0;

    // Declare a trajectory generator to manage the motion of control points. This process is not handled (yet) by the app utility class.
    rkcl::TaskSpaceOTGReflexxes task_space_otg(app.robot(), app.taskSpaceController().controlTimeStep());

    // Initialize the application : start the joint drivers, initialize the processes, and create specific threads to run each driver loop independently
    if (not app.init())
    {
        throw std::runtime_error("Cannot initialize the application");
    }

    // Log the evolution of joint and points data.
    app.addDefaultLogging();

    // Add joint position errors to the logged data
    std::vector<Eigen::VectorXd> joint_position_errors;
    for (size_t i = 0; i < app.robot().jointGroupCount(); ++i)
    {
        Eigen::VectorXd joint_position_error;
        joint_position_error.resize(app.robot().jointGroup(i)->jointCount());
        joint_position_error.setZero();
        joint_position_errors.push_back(joint_position_error);

        app.taskSpaceLogger().log(app.robot().jointGroup(i)->name() + " position error", joint_position_errors[i]);
    }

    // Variable used to indicate if the application should be stopped
    bool stop = false;
    // Variable used to indicate if the current task has been completed
    bool done = false;

    // Allow to use "Ctrl+C" in the terminal to set the "stop" variable to "true"
    pid::SignalManager::registerCallback(pid::SignalManager::Interrupt, "stop", [&stop](int) { stop = true; });

    try
    {

        std::cout << "Starting sand manipulations \n";
        srand(time(NULL));

        // Keep looping until the user wants to stop
        while (not stop)
        {
            // Select and load a random action among the ones specified in the config file
            //auto action_idx = rand() % actions.size();
            auto action_idx = 2; 
            auto action = actions[action_idx];
            auto conf_action = YAML::LoadFile(PID_PATH("app_config/sand_manipulation_simu_config/" + action + ".yaml"));

            app.storeAppConfig(conf_action);
            app.loadTasks();

            // Configure the robot according to the selected action
            app.robot().configure(conf_action["robot"]);
            // Get the number of samples for the selected actions : this is how we divide the sand area (nb_x, nb_y)
            auto nb_samples = conf_action["app"]["nb_samples"].as<std::array<int, 2>>();

            //Randomly select a sample to define the (x,y) position to reach with the hand
            std::array<int, 2> sample;
            sample[0] = rand() % nb_samples[0];
            sample[1] = rand() % nb_samples[1];

            std::cout << "Executing " << action << " at [" << sample[0] << ";" << sample[1] << "] \n";

            // First, set the goal hand pose to reach to be at the origin of the sand area
            auto hand_tcp = app.robot().controlPoint(0);
            hand_tcp->goal().pose().linear() = world_T_sand.linear() * sand_R_hand;
            hand_tcp->goal().pose().translation() = world_T_sand.translation();

            // Get the (dx, dy) translation to apply form the index of the sample
            Eigen::Vector3d sample_translation;
            sample_translation.x() = dim_ws[0] * ((sample[0] + 0.5) / nb_samples[0]);
            sample_translation.y() = dim_ws[1] * ((sample[1] + 0.5) / nb_samples[1]);
            sample_translation.z() = 0;

            // Apply the (dx,dy) translation to the current goal pose to reach the sample in the sand area
            hand_tcp->goal().pose().translation() += world_T_sand.linear() * sample_translation;

            // Load the first task for this action
            app.configureTask(0);

            done = false;

            task_space_otg.reset();

            // Keep looping until the user wants to stop, a problem is detected by the controller, or all tasks for this action have been achieved
            while (not stop and not done)
            {
                // Run one step of the control loop, the first parameter (lambda function) allows to execute some pre-controller code while the second
                // execute some operations at the end of the loop
                bool ok = app.runControlLoop(
                    [&] {
                        if (app.isTaskSpaceControlEnabled())
                            return task_space_otg();
                        else
                            return true;
                    });
                // OK is true if everything went well during the execution of the control loop, false otherwise
                if (ok)
                {
                    // Here we are gonna check if the task has been completed. A task can be define both in the task space and joint space, or only in one of the spaces.
                    done = true;
                    // Task space control is enabled if we want to control the hand control point in the current task
                    if (app.isTaskSpaceControlEnabled())
                    {
                        //For this control point, we evaluate if the destination has been reached, considering a threshold value on the norm of the error between
                        //the current pose and the pose to reach
                        auto cp_ptr = std::static_pointer_cast<rkcl::ControlPoint>(app.robot().controlPoint(0));

                        auto error = rkcl::internal::computePoseError(cp_ptr->goal().pose(), cp_ptr->state().pose());
                        auto error_norm = (static_cast<Eigen::Matrix<double, 6, 6>>(cp_ptr->selectionMatrix().positionControl()) * error).norm();
                        done &= (error_norm < 0.01);
                    }
                    // Joint space control enabled means for at least one joint group the objective is defined in the joint space
                    if (app.isJointSpaceControlEnabled())
                    {
                        size_t joint_index = 0;
                        // Each joint group is given to a joint space trajectory generator which manages its motion, so we evaluate for each joint space trajectory generator
                        for (const auto& joint_space_otg : app.jointSpaceOTGs())
                        {
                            // Evaluate if the joint group is currently controlled in the joint space
                            if (joint_space_otg->jointGroup()->controlSpace() == rkcl::JointGroup::ControlSpace::JointSpace)
                            {
                                // Evaluate if the joint group is position controlled (i.e. the goal is to reach a specific joint configuration)
                                if (joint_space_otg->controlMode() == rkcl::JointSpaceOTG::ControlMode::Position)
                                {
                                    // This joint group has reached the destination if the error norm between the current and goal position is below the threshold
                                    joint_position_errors[joint_index] = joint_space_otg->jointGroup()->selectionMatrix().value() * (joint_space_otg->jointGroup()->goal().position() - joint_space_otg->jointGroup()->state().position());
                                    done &= (joint_position_errors[joint_index].norm() < 0.2);
                                }
                                // Evaluate if the joint group is velocity controlled (i.e. the goal is to reach a specific joint velocity)
                                else if (joint_space_otg->controlMode() == rkcl::JointSpaceOTG::ControlMode::Velocity)
                                {
                                    // This joint group has reached the desired velocity if the error between the current and targeted is behind a given threshold
                                    auto joint_group_error_vel_goal = joint_space_otg->jointGroup()->selectionMatrix().value() * (joint_space_otg->jointGroup()->goal().velocity() - joint_space_otg->jointGroup()->state().velocity());
                                    done &= (joint_group_error_vel_goal.norm() < 1e-10);
                                }
                            }
                        }
                        joint_index++;
                    }
                }
                else
                {
                    throw std::runtime_error("Something wrong happened in the control loop, aborting");
                }
                // If the current task has been completed
                if (done)
                {
                    // We reset "done" to false, in case there is another task to perform
                    done = false;
                    std::cout << "Task completed, moving to the next one" << std::endl;
                    // Try to load the next task specified in the configuration file. Return "false" is there is no more task.
                    done = not app.nextTask();
                    task_space_otg.reset();
                }
            }
        }
        // Stop became "true" is the user pressed "Ctrl+C" in the terminal
        if (stop)
            throw std::runtime_error("Caught user interruption, aborting");
    }
    // Catch a runtime error, if there was one
    catch (const std::exception& e)
    {
        std::cerr << e.what() << std::endl;
    }

    pid::SignalManager::unregisterCallback(pid::SignalManager::Interrupt, "stop");

    std::cout << "Ending the application" << std::endl;

    // Manage the ending oh the application : stop the robot motion, stop the communication with the different drivers
    if (app.end())
        std::cout << "Application ended properly" << std::endl;
    else
        std::cout << "Application ended badly" << std::endl;
    return 0;
}
