## Our buildserver is currently running on: ##

> Ubuntu 16.04.1 LTS 

## openDroid 6.8 is build using oe-alliance build-environment and several git repositories: ##

> [https://github.com/oe-alliance/oe-alliance-core/tree/4.3](https://github.com/oe-alliance/oe-alliance-core/tree/4.3 "OE-Alliance")
> 
> [https://github.com/opendroid-Team/enigma2]  (https://github.com/opendroid-Team/enigma2 "openDroid Enigma2")
> 
> [https://github.com/stein17/Skins-for-openOPD](https://github.com/stein17/Skins-for-openOPD "openDroid Skin")

> and a lot more...


----------

# Building Instructions #

1 - Install packages on your buildserver

    sudo apt-get install -y psmisc autoconf automake bison bzip2 curl cvs diffstat flex g++ gawk gcc gettext git gzip help2man ncurses-bin libncurses5-dev libc6-dev libtool make texinfo patch perl pkg-config subversion tar texi2html wget zlib1g-dev chrpath libxml2-utils xsltproc libglib2.0-dev python-setuptools zip info coreutils diffstat chrpath libproc-processtable-perl libperl4-corelibs-perl sshpass default-jre default-jre-headless java-common libserf-dev qemu quilt libssl-dev
2 - Set your shell to /bin/bash.

    sudo dpkg-reconfigure dash
    When asked: Install dash as /bin/sh?
    select "NO"

----------

3 - modify max_user_watches

    echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf

    sysctl -n -w fs.inotify.max_user_watches=524288

----------

3 - Add user opendroidbuilder

    sudo adduser opendroidbuilder

----------
4 - Switch to user opendroidbuilder

    su opendroidbuilder

----------
5 - Switch to home of openadroidbuilder

    cd ~

----------
6 - Create folder opendroid

    mkdir -p ~/opendroid

----------
7 - Switch to folder opendroid

    cd opendroid

----------
8 - Clone oe-alliance git

    git clone git://github.com/oe-alliance/build-enviroment.git -b 4.3

----------
9 - Switch to folder build-enviroment

    cd build-enviroment

----------
10 - Update build-enviroment

    make update

----------
11 - Finally you can start building a image

    MACHINE=sf4008 DISTRO=opendroid make image
