#include <rkcl/robots/bazar.h>
#include <rkcl/drivers/shadow_hand_driver.h>
#include <rkcl/processors/otg_reflexxes.h>
#include <rkcl/processors/app_utility.h>
#include <yaml-cpp/yaml.h>
#include <pid/rpath.h>
#include <pid/signal_manager.h>

void printWorkspaceParameters(const std::array<Eigen::Vector3d, 3>& workspace_positions)
{
    Eigen::Vector3d rx = workspace_positions[1] - workspace_positions[0];
    //We consider x,y axis on the horizontal plane
    rx.z() = 0;
    rx.normalize();
    // Eigen::Vector3d ry = (workspace_positions[2] - workspace_positions[0]).normalized();
    Eigen::Vector3d rz;
    rz << 0, 0, 1;

    Eigen::Vector3d ry = rz.cross(rx);

    Eigen::Matrix3d rot;
    rot << rx, ry, rz;
    Eigen::Quaterniond q(rot);

    std::cout << "Workspace calibration completed !" << std::endl;
    std::cout << "Reference frame (top left corner expressed in the world) : " << std::endl;
    std::cout << "Position : " << workspace_positions[0].transpose() << std::endl;
    std::cout << "Quaternion : " << q.coeffs().transpose() << std::endl;
    std::cout << "Horizontal dimensions of the operational space : " << std::endl;
    std::cout << "dx = " << abs(workspace_positions[1](0) - workspace_positions[0](0)) << std::endl;
    std::cout << "dy = " << abs(workspace_positions[2](1) - workspace_positions[0](1)) << std::endl;
}

int main()
{
    //TODO : Generate (in a file or console) the reference pose (e.g top left corner) + dimensions of the workspace (length + width)
    rkcl::DriverFactory::add<rkcl::ShadowHandDriver>("shadow");
    rkcl::DriverFactory::add<rkcl::KukaLWRFRIDriver>("fri");

    rkcl::QPSolverFactory::add<rkcl::OSQPSolver>("osqp");

    auto conf = YAML::LoadFile(PID_PATH("app_config/workspace_calibration_init_config.yaml"));
    auto app = rkcl::AppUtility::create<rkcl::ForwardKinematicsRBDyn, rkcl::JointSpaceOTGReflexxes>(conf);
    // app.add<rkcl::CollisionAvoidanceSCH>();

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

    rkcl::PointWrenchEstimator tcp_wrench_estimator(app.robot(), conf["tcp_wrench_estimator"]);

    bool stop = false;
    bool done = false;

    pid::SignalManager::registerCallback(pid::SignalManager::Interrupt, "stop", [&stop](int) { stop = true; });
    pid::SignalManager::registerCallback(pid::SignalManager::UserDefined1, "next", [&done](int) { done = true; });

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
                    done &= (joint_position_errors[i].norm() < 0.1);
                    // if (i == 0)
                    //     std::cout << "error = " << joint_position_errors[i].norm() << "\n";
                }
            }
            else
            {
                throw std::runtime_error("Something wrong happened in the control loop, aborting");
            }
        }

        std::cout << "Initial configuration reached!" << std::endl;
        done = not app.nextTask();
        std::string common_direction(" with the shadow index finger, then press on the thumb to validate");
        std::array<std::string, 3> task_directions{"Go to bottom left corner" + common_direction, "Go to bottom right corner" + common_direction, "Go to top left corner" + common_direction};
        std::array<Eigen::Vector3d, 3> workspace_positions;
        size_t task_idx = 0;
        auto shadow_index_tip = app.robot().observationPoint("shadow_index_tip");
        auto shadow_joint_group = app.robot().jointGroup("shadow_hand");
        std::cout << task_directions[0] << std::endl;
        while (not stop and not done)
        {
            bool ok = app.runControlLoop([&] {
                return tcp_wrench_estimator();
            });

            if (ok)
            {
                for (size_t i = 0; i < app.robot().jointGroupCount(); ++i)
                {
                    auto joint_group = app.robot().jointGroup(i);
                    joint_position_errors[i] = joint_group->selectionMatrix().value() * (joint_group->goal().position() - joint_group->state().position());
                }
                done = (abs(shadow_joint_group->state().force()(13)) > 300);
            }
            else
            {
                throw std::runtime_error("Something wrong happened in the control loop, aborting");
            }
            if (done)
            {
                workspace_positions[task_idx] = shadow_index_tip->state().pose().translation();
                std::cout << "Location stored, Please release the thumb" << std::endl;
                std::this_thread::sleep_for(std::chrono::seconds(2));

                if (task_idx < (task_directions.size() - 1))
                {
                    task_idx++;
                    std::cout << task_directions[task_idx] << std::endl;
                    done = false;
                }
                else
                {
                    std::cout << "All points recorded. Computing the workspace parameters..." << std::endl;
                    printWorkspaceParameters(workspace_positions);
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
