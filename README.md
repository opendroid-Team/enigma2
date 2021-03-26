## Build Status - branch 7.1  develop: ##
[![Build Status](https://travis-ci.org/opendroid-Team/enigma2.svg?branch=7.1)](https://travis-ci.org/opendroid-Team/enigma2)

## Our buildserver is currently running on: ##

> Ubuntu 20.04.1 LTS (Kernel 5.4.0)

## openDroid 7.1 is build using oe-alliance build-environment and several git repositories: ##

> [https://github.com/oe-alliance/oe-alliance-core/tree/nextp3](https://github.com/oe-alliance/oe-alliance-core/tree/nextp3 "OE-Alliance")
> 
> [https://github.com/opendroid-Team/enigma2](https://github.com/opendroid-Team/enigma2/tree/7.1 "openDroid Enigma2")
> 
> [https://github.com/stein17/Skins-for-openOPD](https://github.com/stein17/Skins-for-openOPD "openDroid Skin")

> and a lot more...


----------

# Building Instructions #

1 - Install packages on your buildserver

    sudo apt-get install -y autoconf automake bison bzip2 chrpath coreutils cpio curl cvs debianutils default-jre default-jre-headless diffstat flex g++ gawk gcc gcc-8 gcc-multilib g++-multilibgettext git git-core gzip help2man info iputils-ping java-common libc6-dev libegl1-mesa libglib2.0-dev libncurses5-dev libperl4-corelibs-perl libproc-processtable-perl libsdl1.2-dev libserf-dev libtool libxml2-utils make ncurses-bin patch perl pkg-config psmisc python3 python3-git python3-jinja2 python3-pexpect python3-pip python-setuptools qemu quilt socat sshpass subversion tar texi2html texinfo unzip wget xsltproc xterm xz-utils zip zlib1g-dev 
    
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

5 - Add user opendroidbuilder

    sudo adduser opendroidbuilder

----------
6 - Switch to user opendroidbuilder

    su opendroidbuilder

----------
7 - Switch to home of openadroidbuilder

    cd ~

----------
8 - Create folder opendroid

    mkdir -p ~/opendroid

----------
9 - Switch to folder opendroid

    cd opendroid

----------
10 - Clone oe-alliance git

    git clone git://github.com/oe-alliance/build-enviroment.git -b nextp3

----------
11 - Switch to folder build-enviroment

    cd build-enviroment

----------
12 - Update build-enviroment

    make update

----------
13 - Finally you can start building a image

    MACHINE=sf4008 DISTRO=opendroid make image
