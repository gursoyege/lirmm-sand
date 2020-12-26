declare_PID_Component(
    APPLICATION
    NAME workspace-calibration
    DIRECTORY workspace_calibration
    RUNTIME_RESOURCES app_config app_log app_model
    DEPEND
        rkcl-bazar-robot/rkcl-bazar-robot
        rkcl-driver-vrep/rkcl-driver-vrep
        rkcl-otg-reflexxes/rkcl-otg-reflexxes
        pid-rpath/rpathlib
        pid-os-utilities/pid-signal-manager
        rkcl-app-utility/rkcl-app-utility
        rkcl-driver-shadow-hand/rkcl-driver-shadow-hand
)
