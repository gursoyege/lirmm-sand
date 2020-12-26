#include <rkcl/robots/bazar.h>
#include <rkcl/processors/app_utility.h>
#include <rkcl/processors/otg_reflexxes.h>
#include <rkcl/drivers/vrep_driver.h>
#include <rkcl/processors/internal/internal_functions.h>
#include <pid/signal_manager.h>

int main(int argc, char* argv[])
{
    rkcl::DriverFactory::add<rkcl::VREPMainDriver>("vrep_main");
    rkcl::DriverFactory::add<rkcl::VREPJointDriver>("vrep_joint");
    rkcl::QPSolverFactory::add<rkcl::OSQPSolver>("osqp");

    auto conf = YAML::LoadFile(PID_PATH("app_config/simple_simu_init_config.yaml"));

    auto app = rkcl::AppUtility::create<rkcl::ForwardKinematicsRBDyn, rkcl::JointSpaceOTGReflexxes>(conf);

    rkcl::TaskSpaceOTGReflexxes task_space_otg(app.robot(), app.taskSpaceController().controlTimeStep());

    if (not app.init())
    {
        throw std::runtime_error("Cannot initialize the application");
    }

    app.addDefaultLogging();

    bool stop = false;
    bool done = false;

    pid::SignalManager::registerCallback(pid::SignalManager::Interrupt, "stop",
                                         [&](int) { stop = true; });

    try
    {
        std::cout << "Starting control loop \n";
        app.configureTask(0);
        task_space_otg.reset();
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
                if (app.isTaskSpaceControlEnabled())
                {
                    double error_norm = 0;
                    for (size_t i = 0; i < app.robot().controlPointCount(); ++i)
                    {
                        auto cp_ptr = std::static_pointer_cast<rkcl::ControlPoint>(app.robot().controlPoint(i));
                        auto error = rkcl::internal::computePoseError(cp_ptr->goal().pose(), cp_ptr->state().pose());
                        // error_norm += (static_cast<Eigen::Matrix<double, 6, 6>>(cp_ptr->positionControlSelectionMatrix()) * error).norm();
                        error_norm += (cp_ptr->selectionMatrix().positionControl() * error).norm();
                    }

                    done &= (error_norm < 0.01);
                }
                if (app.isJointSpaceControlEnabled())
                {
                    for (const auto& joint_space_otg : app.jointSpaceOTGs())
                    {
                        if (joint_space_otg->jointGroup()->controlSpace() == rkcl::JointGroup::ControlSpace::JointSpace)
                        {
                            if (joint_space_otg->controlMode() == rkcl::JointSpaceOTG::ControlMode::Position)
                            {
                                // auto joint_group_error_pos_goal = joint_space_otg->jointGroup()->selectionMatrix().value() * (joint_space_otg->jointGroup()->goal().position() - joint_space_otg->jointGroup()->state().position());
                                // done &= (joint_group_error_pos_goal.norm() < 0.001);
                                done &= joint_space_otg->finalStateReached();
                            }
                            else if (joint_space_otg->controlMode() == rkcl::JointSpaceOTG::ControlMode::Velocity)
                            {
                                auto joint_group_error_vel_goal = joint_space_otg->jointGroup()->selectionMatrix().value() * (joint_space_otg->jointGroup()->goal().velocity() - joint_space_otg->jointGroup()->state().velocity());
                                done &= (joint_group_error_vel_goal.norm() < 1e-10);
                            }
                        }
                    }
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
            }
        }
        if (stop)
            throw std::runtime_error("Caught user interruption, aborting");

        std::cout << "All tasks completed" << std::endl;
    }
    catch (const std::exception& e)
    {
        std::cerr << e.what() << std::endl;
    }

    pid::SignalManager::unregisterCallback(pid::SignalManager::Interrupt, "stop");

    app.end();
}
