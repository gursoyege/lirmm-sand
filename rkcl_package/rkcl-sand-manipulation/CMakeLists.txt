CMAKE_MINIMUM_REQUIRED(VERSION 3.0.2)
set(WORKSPACE_DIR ${CMAKE_SOURCE_DIR}/../.. CACHE PATH "root of the PID workspace directory")
list(APPEND CMAKE_MODULE_PATH ${WORKSPACE_DIR}/share/cmake/system) # using generic scripts/modules of the workspace
include(Package_Definition NO_POLICY_SCOPE)
option(REAL_ROBOT "Build the applications that are run on the real robot" OFF)

project(rkcl-sand-manipulation)

PID_Package(
			AUTHOR          Sonny Tarbouriech
			INSTITUTION	    LIRMM
			ADDRESS 		git@gite.lirmm.fr:rkcl/rkcl-sand-manipulation.git
			PUBLIC_ADDRESS	https://gite.lirmm.fr/rkcl/rkcl-sand-manipulation.git
			YEAR        	2020
			LICENSE     	CeCILL
			DESCRIPTION 	Application package to perform sand manipulation using the BAZAR robot endowed with a Shadow hand
			CODE_STYLE		rkcl
			VERSION     	2.0.0
		)

PID_Category(application)
PID_Publishing(PROJECT           https://gite.lirmm.fr/rkcl-sand-manipulation
				FRAMEWORK         rkcl-framework
				DESCRIPTION       Application package to perform sand manipulation using the BAZAR robot endowed with a Shadow hand
				ALLOWED_PLATFORMS x86_64_linux_abi11)

PID_Dependency(pid-os-utilities VERSION 2.3.0)
PID_Dependency(pid-rpath VERSION 2.2.1)
PID_Dependency(rkcl-driver-vrep VERSION 2.0.0)
PID_Dependency(rkcl-otg-reflexxes VERSION 2.0.0)
PID_Dependency(rkcl-app-utility VERSION 2.0.0)
PID_Dependency(rkcl-bazar-robot VERSION 2.0.0)

if(REAL_ROBOT)
	PID_Dependency(rkcl-driver-shadow-hand VERSION 2.0.0)
endif()



build_PID_Package()
