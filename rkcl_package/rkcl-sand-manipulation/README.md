
Overview
=========

Application package to perform sand manipulation using the BAZAR robot endowed with a Shadow hand



The license that applies to the whole package content is **CeCILL**. Please look at the license.txt file at the root of this repository.

Installation and Usage
=======================

The detailed procedures for installing the rkcl-sand-manipulation package and for using its components is available in this [site][package_site]. It is based on a CMake based build and deployment system called [PID](http://pid.lirmm.net/pid-framework/pages/install.html). Just follow and read the links to understand how to install, use and call its API and/or applications.

For a quick installation:

## Installing the project into an existing PID workspace

To get last version :
 ```
cd <path to pid workspace>/pid
make deploy package=rkcl-sand-manipulation
```

To get a specific version of the package :
 ```
cd <path to pid workspace>/pid
make deploy package=rkcl-sand-manipulation version=<version number>
```

## Standalone install
 ```
git clone https://gite.lirmm.fr/rkcl/rkcl-sand-manipulation.git
cd rkcl-sand-manipulation
```

Then run the adequate install script depending on your system. For instance on linux:
```
sh share/install/standalone_install.sh
```

The pkg-config tool can be used to get all links and compilation flags for the libraries defined inthe project. To let pkg-config know these libraries, read the last output of the install_script and apply the given command. It consists in setting the PKG_CONFIG_PATH, for instance on linux do:
```
export PKG_CONFIG_PATH=<path to rkcl-sand-manipulation>/binaries/pid-workspace/share/pkgconfig:$PKG_CONFIG_PATH
```

Then, to get compilation flags run:

```
pkg-config --static --cflags rkcl-sand-manipulation_<name of library>
```

To get linker flags run:

```
pkg-config --static --libs rkcl-sand-manipulation_<name of library>
```


About authors
=====================

rkcl-sand-manipulation has been developped by following authors: 
+ Sonny Tarbouriech (LIRMM)

Please contact Sonny Tarbouriech - LIRMM for more information or questions.


[package_site]: http://rkcl.lirmm.net/rkcl-framework/packages/rkcl-sand-manipulation "rkcl-sand-manipulation package"

