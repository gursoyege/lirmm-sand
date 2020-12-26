#include <rkcl/robots/bazar.h>
#include <rkcl/drivers/shadow_hand_driver.h>
#include <rkcl/processors/otg_reflexxes.h>
#include <rkcl/processors/app_utility.h>
#include <rkcl/processors/internal/internal_functions.h>
#include <yaml-cpp/yaml.h>
#include <pid/rpath.h>
#include <pid/signal_manager.h>

int main()
{
    rkcl::DriverFactory::add<rkcl::ShadowHandDriver>("shadow");
    rkcl::DriverFactory::add<rkcl::KukaLWRFRIDriver>("fri");
    rkcl::QPSolverFactory::add<rkcl::OSQPSolver>("osqp");

    auto conf_app = YAML::LoadFile(PID_PATH("app_config/sand_manipulation_init_config.yaml"));
    auto app = rkcl::AppUtility::create<rkcl::ForwardKinematicsRBDyn, rkcl::JointSpaceOTGReflexxes>(conf_app);
    // app.add<rkcl::CollisionAvoidanceSCH>();

    auto actions = conf_app["app"]["actions"].as<std::vector<std::string>>();
    std::vector<Eigen::Vector3d> offset;

    Eigen::Vector3d tap_offset;
    // tap_offset << -0.02, -0.06, 0;
    tap_offset << -0.02, 0.1, 0;
    Eigen::Vector3d grasp_offset = tap_offset;
    Eigen::Vector3d poke_offset = tap_offset;

    offset.push_back(tap_offset);
    offset.push_back(grasp_offset);
    offset.push_back(poke_offset);

    auto conf_ws_calibration = YAML::LoadFile(PID_PATH("app_config/workspace_calibration_data.yaml"));
    Eigen::Affine3d world_T_sand;
    Eigen::Vector3d position(conf_ws_calibration["reference_position"].as<std::vector<double>>().data());
    Eigen::Quaterniond quat(conf_ws_calibration["reference_quaternion"].as<std::vector<double>>().data());
    world_T_sand.translation() = position;
    world_T_sand.linear() = quat.matrix();
    auto dim_ws = conf_ws_calibration["dimension"].as<std::array<double, 2>>();

    Eigen::Matrix3d sand_R_hand;
    sand_R_hand << -1, 0, 0,
        0, 0, 1,
        0, 1, 0;
    rkcl::TaskSpaceOTGReflexxes task_space_otg(app.robot(), app.taskSpaceController().controlTimeStep());

    if (not app.init())
    {
        throw std::runtime_error("Cannot initialize the application");
    }

    app.addDefaultLogging();

    std::vector<Eigen::VectorXd> joint_position_errors;
    for (size_t i = 0; i < app.robot().jointGroupCount(); ++i)
    {
        Eigen::VectorXd joint_position_error;
        joint_position_error.resize(app.robot().jointGroup(i)->jointCount());
        joint_position_error.setZero();
        joint_position_errors.push_back(joint_position_error);

        app.taskSpaceLogger().log(app.robot().jointGroup(i)->name() + " position error", joint_position_errors[i]);
    }

    bool stop = false;
    bool done = false;

    pid::SignalManager::registerCallback(pid::SignalManager::Interrupt, "stop", [&stop](int) { stop = true; });

    try
    {
        std::cout << "Going to initial configuration... \n";
        app.configureTask(0);
        while (not stop and not done)
        {
            bool ok = app.runControlLoop();

            if (ok)
            {
                done = true;
                for (size_t i = 0; i < app.robot().jointGroupCount(); ++i)
                {
                    auto joint_group = app.robot().jointGroup(i);
                    joint_position_errors[i] = joint_group->selectionMatrix().value() * (joint_group->goal().position() - joint_group->state().position());
                    done &= (joint_position_errors[i].norm() < 0.2);
                }
            }
            else
            {
                throw std::runtime_error("Something wrong happened in the control loop, aborting");
            }
        }

        std::cout << "Starting sand manipulations \n";
        srand(time(NULL));

        while (not stop)
        {

            // auto action_idx = rand() % actions.size();
            auto action_idx = 2;
            auto action = actions[action_idx];
            auto conf_action = YAML::LoadFile(PID_PATH("app_config/sand_manipulation_config/" + action + ".yaml"));

            app.storeAppConfig(conf_action);
            app.loadTasks();

            app.robot().configure(conf_action["robot"]);
            auto nb_samples = conf_action["app"]["nb_samples"].as<std::array<int, 2>>();

            std::array<int, 2> sample;
            // sample[0] = rand() % nb_samples[0];
            // sample[1] = rand() % nb_samples[1];

            for (auto x_sample = 2; x_sample < nb_samples[0] - 2; ++x_sample)
            {
                for (auto y_sample = 0; y_sample < nb_samples[1]; ++y_sample)
                {

                    sample[0] = x_sample;
                    sample[1] = y_sample;

                    // sample[0] = nb_samples[0] - 1;
                    // sample[1] = nb_samples[1] - 1;

                    auto hand_tcp = app.robot().controlPoint(0);
                    // hand_tcp->goal.pose = world_T_sand;
                    hand_tcp->goal().pose().linear() = world_T_sand.linear() * sand_R_hand;
                    hand_tcp->goal().pose().translation() = world_T_sand.translation();

                    Eigen::Vector3d sample_translation;
                    sample_translation.x() = dim_ws[0] * ((sample[0] + 0.5) / nb_samples[0]);
                    sample_translation.y() = dim_ws[1] * ((sample[1] + 0.5) / nb_samples[1]);
                    sample_translation.z() = 0;

                    // std::cout << "goal.pose.translation = " << hand_tcp->goal.pose.translation().transpose() << "\n";
                    // std::cout << "sample_translation = " << sample_translation.transpose() << "\n";
                    // std::cout << "hand_tcp->goal.pose.linear() = \n"
                    //           << hand_tcp->goal.pose.linear() << "\n";

                    hand_tcp->goal().pose().translation() += world_T_sand.linear() * (sample_translation + offset[action_idx]);

                    // hand_tcp->goal.pose.translation() += offset[action_idx]

                    // std::cout << "goal.pose.translation = " << hand_tcp->goal.pose.translation().transpose() << "\n";

                    app.configureTask(0);

                    // std::cout << "goal.pose.translation = " << hand_tcp->goal.pose.translation().transpose() << "\n\n";

                    done = false;

                    task_space_otg.reset();

                    std::chrono::high_resolution_clock::time_point time_wrench_threshold_detected = std::chrono::high_resolution_clock::now();
                    std::chrono::high_resolution_clock::time_point time_task_started = std::chrono::high_resolution_clock::now();

                    while (not stop and not done)
                    {

                        bool ok = app.runControlLoop(
                            [&] {
                                if (app.isTaskSpaceControlEnabled())
                                    return task_space_otg();
                                else
                                    return true;
                            });

                        if (ok)
                        {
                            done = true;
                            auto duration_wrench = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now() - time_wrench_threshold_detected).count();
                            auto duration_task = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now() - time_task_started).count();
                            if ((abs(hand_tcp->state().wrench()(2)) < 40 || duration_wrench < 1e6) && duration_task < 30e6)
                            {
                                if (app.isTaskSpaceControlEnabled())
                                {
                                    double error_norm = 0;
                                    for (size_t i = 0; i < app.robot().controlPointCount(); ++i)
                                    {
                                        auto cp_ptr = std::static_pointer_cast<rkcl::ControlPoint>(app.robot().controlPoint(i));
                                        if (cp_ptr->isEnabled())
                                        {
                                            auto error = rkcl::internal::computePoseError(cp_ptr->goal().pose(), cp_ptr->state().pose());
                                            error_norm += (static_cast<Eigen::Matrix<double, 6, 6>>(cp_ptr->positionControlSelectionMatrix()) * error).norm();
                                        }
                                    }
                                    done &= (error_norm < 0.01);
                                }
                                if (app.isJointSpaceControlEnabled())
                                {
                                    size_t joint_index = 0;
                                    for (const auto& joint_space_otg : app.jointSpaceOTGs())
                                    {
                                        if (joint_space_otg->jointGroup()->controlSpace() == rkcl::JointGroup::ControlSpace::JointSpace)
                                        {
                                            if (joint_space_otg->controlMode() == rkcl::JointSpaceOTG::ControlMode::Position)
                                            {
                                                joint_position_errors[joint_index] = joint_space_otg->jointGroup()->selectionMatrix().value() * (joint_space_otg->jointGroup()->goal().position() - joint_space_otg->jointGroup()->state().position());
                                                done &= (joint_position_errors[joint_index].norm() < 0.2);
                                                // std::cout << "error = " << joint_position_errors[joint_index].transpose() << "\n";
                                            }
                                            else if (joint_space_otg->controlMode() == rkcl::JointSpaceOTG::ControlMode::Velocity)
                                            {
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
                                if (abs(hand_tcp->state().wrench()(2)) >= 40)
                                {
                                    time_wrench_threshold_detected = std::chrono::high_resolution_clock::now();
                                    std::cout << "wrench norm reached the threshold ----------------------- \n";
                                }
                                else
                                    std::cout << "Task time out !  ----------------------- \n";
                            }
                        }
                        else
                        {
                            throw std::runtime_error("Something wrong happened in the control loop, aborting");
                        }
                        if (done)
                        {
                            done = false;
                            std::cout << "Task completed, moving to the next one" << std::endl;
                            done = not app.nextTask();
                            task_space_otg.reset();
                            time_task_started = std::chrono::high_resolution_clock::now();
                        }
                    }
                }
            }
        }
        if (stop)
            throw std::runtime_error("Caught user interruption, aborting");
    }
    catch (const std::exception& e)
    {
        std::cerr << e.what() << std::endl;
    }

    pid::SignalManager::unregisterCallback(pid::SignalManager::Interrupt, "stop");

    std::cout << "Ending the application" << std::endl;

    if (app.end())
        std::cout << "Application ended properly" << std::endl;
    else
        std::cout << "Application ended badly" << std::endl;
    return 0;
}
