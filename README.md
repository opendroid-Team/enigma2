## Build Status - branch 7.3  develop: ##

## Our buildserver is currently running on: ##

## Current OS

> Ubuntu 24.04 LTS (GNU/Linux 6.8.0-31-generic x86_64)

## Hardware requirements

> RAM:  16GB
>
> SWAP: 8GB
>
> CPU:  Multi core\thread Model
>
> HDD:  for Single Build 250GB Free, for Multibuild 500GB or more

## openDroid 7.3 is build using oe-alliance build-environment and several git repositories: ##

> [OE Alliance Core](https://github.com/oe-alliance/oe-alliance-core/tree/5.5 "OE Alliance Core") - Core framework
> 
> [https://github.com/opendroid-Team/enigma2](https://github.com/opendroid-Team/enigma2/tree/7.3 "openDroid Enigma2")
> 
> [https://github.com/stein17/Skins-for-openOPD/tree/python3)

> and a lot more...


----------

# Building Instructions #

1 - Install packages on your buildserver

    sudo apt-get install -y autoconf automake bison bzip2 chrpath coreutils cpio curl cvs debianutils default-jre default-jre-headless diffstat flex g++ gawk gcc gcc-12 gcc-multilib g++-multilib gettext git gzip help2man info iputils-ping java-common libc6-dev libglib2.0-dev libncurses-dev libperl4-corelibs-perl libproc-processtable-perl libsdl1.2-dev libserf-dev libtool libxml2-utils make ncurses-bin patch perl pkg-config psmisc python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-setuptools quilt socat sshpass subversion tar texi2html texinfo unzip wget xsltproc xterm xz-utils zip zlib1g-dev zstd fakeroot lz4 git-lfs

----------
2 - Set python3 as preferred provider for python

    sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 1
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 2
    sudo update-alternatives --config python
    select python3

----------
3 - Set your shell to /bin/bash.

    sudo dpkg-reconfigure dash
    When asked: Install dash as /bin/sh?
    select "NO"

----------
4 - modify max_user_watches

    echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf

    sudo sysctl -n -w fs.inotify.max_user_watches=524288

----------

1. Disable apparmor profile

    ```sh
    sudo apparmor_parser -R /etc/apparmor.d/unprivileged_userns

    sudo mv /etc/apparmor.d/unprivileged_userns /etc/apparmor.d/disable

    ```sh

2 - Add user opendroidbuilder

    sudo adduser opendroidbuilder

----------
3 - Switch to user opendroidbuilder

    su opendroidbuilder

----------
4 - Switch to home of openadroidbuilder

    cd ~

----------
5 - Create folder opendroid

    mkdir -p ~/opendroid

----------
6 - Switch to folder opendroid

    cd opendroid

----------
7 - Clone oe-alliance git

    git clone git://github.com/oe-alliance/build-enviroment.git -b 5.5

----------
8 - Switch to folder build-enviroment

    cd build-enviroment

----------
9 - Update build-enviroment

    make update

----------
10 - Finally you can start building a image

* Build an image with feed (build time 5-12h)

    ```sh
11 -    MACHINE=sf4008 DISTRO=opendroid DISTRO_TYPE=release make image
    ```

> Build an image without feed (build time 1-2h)

    ```sh
12 -    MACHINE=sf4008 DISTRO=opendroid DISTRO_TYPE=release make enigma2-image
    ```

> Build the feeds

    ```sh
    MACHINE=sf4008 DISTRO=opendroid DISTRO_TYPE=release make feeds
    ```

> Build specific packages

    ```sh
13 -    MACHINE=sf4008 DISTRO=opendroid DISTRO_TYPE=release make init

    cd builds/opendroid/sf4008/

    source env.source

    bitbake nfs-utils rpcbind ...
