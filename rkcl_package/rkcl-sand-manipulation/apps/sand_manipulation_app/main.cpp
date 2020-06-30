#include <rkcl/robots/bazar.h>
#include <rkcl/drivers/vrep_driver.h>
#include <rkcl/processors/vrep_visualization.h>
#include <rkcl/processors/joint_space_otg_reflexxes.h>
#include <rkcl/processors/task_space_otg_reflexxes.h>
#include <rkcl/processors/app_utility.h>
#include <yaml-cpp/yaml.h>
#include <pid/rpath.h>
#include <pid/signal_manager.h>

int main()
{
    rkcl::DriverFactory::add<rkcl::VREPMainDriver>("vrep_main");
    rkcl::DriverFactory::add<rkcl::VREPJointDriver>("vrep_joint");
    rkcl::QPSolverFactory::add<rkcl::OSQPSolver>("osqp");

    //----------- Load config ------------

    int loc, act, dir;
    YAML::Node conf;

    std::cout << "Select location: 1.top-left 2.top-right 3.bottom-left 4.bottom-right" << std::endl;
    std::cin >> loc;
    
    if (loc == 1) // TL
    {
        std::cout << "Select action: 1.claw_closed 2.claw_open 3.pinch 4.poke 5.tap" << std::endl;
        std::cin >> act;
        if (act == 1) // claw_closed
        {
            std::cout << "Select direction: 1.West 2.SouthWest 3.South 4.SouthEast 5.East" << std::endl;
            std::cin >> dir;
            if (dir == 1)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TL/claw_closed/TL_claw_closed_W.yaml"));
            }
            else if (dir == 2)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TL/claw_closed/TL_claw_closed_SW.yaml"));
            }
            else if (dir == 3)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TL/claw_closed/TL_claw_closed_S.yaml"));
            }
            else if (dir == 4)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TL/claw_closed/TL_claw_closed_SE.yaml"));
            }
            else if (dir == 5)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TL/claw_closed/TL_claw_closed_E.yaml"));
            }
            else
            {
                std::cout << "Incorrect number" << std::endl;
                return 0;
            }
        }
        else if (act == 2) // claw_open
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/TL/claw_open/TL_claw_open.yaml"));
        }
        else if (act == 3) //pinch
        {
            std::cout << "Select tilt angle: 1. 0deg 2. 30deg 3. 60deg" << std::endl;
            std::cin >> dir;
            if (dir == 1)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TL/pinch/TL_pinch_0deg.yaml"));
            }
            else if (dir == 2)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TL/pinch/TL_pinch_30deg.yaml"));
            }
            else if (dir == 3)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TL/pinch/TL_pinch_60deg.yaml"));
            }
            else
            {
                std::cout << "Incorrect number" << std::endl;
                return 0;                
            }
        }
        else if (act == 4) // poke
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/TL/poke/TL_poke.yaml"));
        }
        else if (act == 5) // tap
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/TL/tap/TL_tap.yaml"));
        }
        else
        {
            std::cout << "Incorrect number" << std::endl;
            return 0;  
        }
    }
    else if (loc == 2) // TR
    {
        std::cout << "Select action: 1.claw_closed 2.claw_open 3.pinch 4.poke 5.tap" << std::endl;
        std::cin >> act;
        if (act == 1) // claw_closed
        {
            std::cout << "Select direction: 1.West 2.SouthWest 3.South 4.SouthEast 5.East" << std::endl;
            std::cin >> dir;
            if (dir == 1)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TR/claw_closed/TR_claw_closed_W.yaml"));
            }
            else if (dir == 2)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TR/claw_closed/TR_claw_closed_SW.yaml"));
            }
            else if (dir == 3)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TR/claw_closed/TR_claw_closed_S.yaml"));
            }
            else if (dir == 4)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TR/claw_closed/TR_claw_closed_SE.yaml"));
            }
            else if (dir == 5)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TR/claw_closed/TR_claw_closed_E.yaml"));
            }
            else
            {
                std::cout << "Incorrect number" << std::endl;
                return 0;
            }
        }
        else if (act == 2) // claw_open
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/TR/claw_open/TR_claw_open.yaml"));
        }
        else if (act == 3) //pinch
        {
            std::cout << "Select tilt angle: 1. 0deg 2. 30deg 3. 60deg" << std::endl;
            std::cin >> dir;
            if (dir == 1)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TR/pinch/TR_pinch_0deg.yaml"));
            }
            else if (dir == 2)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TR/pinch/TR_pinch_30deg.yaml"));
            }
            else if (dir == 3)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/TR/pinch/TR_pinch_60deg.yaml"));
            }
            else
            {
                std::cout << "Incorrect number" << std::endl;
                return 0;                
            }
        }
        else if (act == 4) // poke
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/TR/poke/TR_poke.yaml"));
        }
        else if (act == 5) // tap
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/TR/tap/TR_tap.yaml"));
        }
        else
        {
            std::cout << "Incorrect number" << std::endl;
            return 0;  
        }
    }
    else if (loc == 3) // BL
    {
        std::cout << "Select action: 1.claw_closed 2.claw_open 3.pinch 4.poke 5.tap" << std::endl;
        std::cin >> act;
        if (act == 1) // claw_closed
        {
            std::cout << "Select direction: 1.West 2.SouthWest 3.South 4.SouthEast 5.East" << std::endl;
            std::cin >> dir;
            if (dir == 1)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BL/claw_closed/BL_claw_closed_W.yaml"));
            }
            else if (dir == 2)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BL/claw_closed/BL_claw_closed_SW.yaml"));
            }
            else if (dir == 3)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BL/claw_closed/BL_claw_closed_S.yaml"));
            }
            else if (dir == 4)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BL/claw_closed/BL_claw_closed_SE.yaml"));
            }
            else if (dir == 5)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BL/claw_closed/BL_claw_closed_E.yaml"));
            }
            else
            {
                std::cout << "Incorrect number" << std::endl;
                return 0;
            }
        }
        else if (act == 2) // claw_open
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/BL/claw_open/BL_claw_open.yaml"));
        }
        else if (act == 3) //pinch
        {
            std::cout << "Select tilt angle: 1. 0deg 2. 30deg 3. 60deg" << std::endl;
            std::cin >> dir;
            if (dir == 1)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BL/pinch/BL_pinch_0deg.yaml"));
            }
            else if (dir == 2)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BL/pinch/BL_pinch_30deg.yaml"));
            }
            else if (dir == 3)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BL/pinch/BL_pinch_60deg.yaml"));
            }
            else
            {
                std::cout << "Incorrect number" << std::endl;
                return 0;                
            }
        }
        else if (act == 4) // poke
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/BL/poke/BL_poke.yaml"));
        }
        else if (act == 5) // tap
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/BL/tap/BL_tap.yaml"));
        }
        else
        {
            std::cout << "Incorrect number" << std::endl;
            return 0;  
        }
    }
    else if (loc == 4) // BR
    {
        std::cout << "Select action: 1.claw_closed 2.claw_open 3.pinch 4.poke 5.tap" << std::endl;
        std::cin >> act;
        if (act == 1) // claw_closed
        {
            std::cout << "Select direction: 1.West 2.SouthWest 3.South 4.SouthEast 5.East" << std::endl;
            std::cin >> dir;
            if (dir == 1)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BR/claw_closed/BR_claw_closed_W.yaml"));
            }
            else if (dir == 2)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BR/claw_closed/BR_claw_closed_SW.yaml"));
            }
            else if (dir == 3)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BR/claw_closed/BR_claw_closed_S.yaml"));
            }
            else if (dir == 4)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BR/claw_closed/BR_claw_closed_SE.yaml"));
            }
            else if (dir == 5)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BR/claw_closed/BR_claw_closed_E.yaml"));
            }
            else
            {
                std::cout << "Incorrect number" << std::endl;
                return 0;
            }
        }
        else if (act == 2) // claw_open
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/BR/claw_open/BR_claw_open.yaml"));
        }
        else if (act == 3) //pinch
        {
            std::cout << "Select tilt angle: 1. 0deg 2. 30deg 3. 60deg" << std::endl;
            std::cin >> dir;
            if (dir == 1)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BR/pinch/BR_pinch_0deg.yaml"));
            }
            else if (dir == 2)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BR/pinch/BR_pinch_30deg.yaml"));
            }
            else if (dir == 3)
            {
                conf = YAML::LoadFile(PID_PATH("app_config/config/BR/pinch/BR_pinch_60deg.yaml"));
            }
            else
            {
                std::cout << "Incorrect number" << std::endl;
                return 0;                
            }
        }
        else if (act == 4) // poke
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/BR/poke/BR_poke.yaml"));
        }
        else if (act == 5) // tap
        {
            conf = YAML::LoadFile(PID_PATH("app_config/config/BR/tap/BR_tap.yaml"));
        }
        else
        {
            std::cout << "Incorrect number" << std::endl;
            return 0;  
        }
    }
    else
    {
        std::cout << "Incorrect number" << std::endl;
        return 0;  
    }

    auto app = rkcl::AppUtility::create<rkcl::ForwardKinematicsRBDyn, rkcl::JointSpaceOTGReflexxes>(conf);
    
    // app.add<rkcl::CollisionAvoidanceSCH>();

    rkcl::TaskSpaceOTGReflexxes task_space_otg(app.getRobot(), app.getTaskSpaceController().getControlTimeStep());

    if (not app.init())
    {
        throw std::runtime_error("Cannot initialize the application");
    }

    app.addDefaultLogging();

    bool stop = false;
    bool done = false;

    pid::SignalManager::registerCallback(pid::SignalManager::Interrupt, "stop", [&stop](int) { stop = true; });

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
                },
                {});

            if (ok)
            {
                done = true;
                if (app.isTaskSpaceControlEnabled())
                {
                    done &= (app.getTaskSpaceController().getControlPointsPoseErrorGoalNormPosition() < 0.05);
                }
                if (app.isJointSpaceControlEnabled())
                {
                    for (const auto& joint_space_otg : app.getJointSpaceOTGs())
                    {
                        if (joint_space_otg->getJointGroup()->control_space == rkcl::JointGroup::ControlSpace::JointSpace)
                        {
                            if (joint_space_otg->getControlMode() == rkcl::JointSpaceOTG::ControlMode::Position)
                            {
                                auto joint_group_error_pos_goal = joint_space_otg->getJointGroup()->selection_matrix * (joint_space_otg->getJointGroup()->goal.position - joint_space_otg->getJointGroup()->state.position);
                                done &= (joint_group_error_pos_goal.norm() < 0.005);
                            }
                            else if (joint_space_otg->getControlMode() == rkcl::JointSpaceOTG::ControlMode::Velocity)
                            {
                                auto joint_group_error_vel_goal = joint_space_otg->getJointGroup()->selection_matrix * (joint_space_otg->getJointGroup()->goal.velocity - joint_space_otg->getJointGroup()->state.velocity);
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

    std::cout << "Ending the application" << std::endl;
    rkcl::VREPMainDriver::notifyStop();

    if (app.end())
        std::cout << "Application ended properly" << std::endl;
    else
        std::cout << "Application ended badly" << std::endl;
    return 0;
}
