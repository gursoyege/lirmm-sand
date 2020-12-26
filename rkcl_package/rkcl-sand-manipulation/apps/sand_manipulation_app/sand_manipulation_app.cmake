declare_PID_Component(
    APPLICATION
    NAME sand-manipulation-app
    DIRECTORY sand_manipulation_app
    RUNTIME_RESOURCES app_config app_log app_model
    DEPEND
        rkcl-bazar-robot/rkcl-bazar-robot
        rkcl-otg-reflexxes/rkcl-otg-reflexxes
        pid-rpath/rpathlib
        pid-os-utilities/pid-signal-manager
        rkcl-app-utility/rkcl-app-utility
        rkcl-driver-shadow-hand/rkcl-driver-shadow-hand
)
