## Our buildserver is currently running on: ##

> Ubuntu 15.10 

## openDroid 5.5 is build using oe-alliance build-environment and several git repositories: ##

> [https://github.com/oe-alliance/oe-alliance-core]
> 
> [https://github.com/opendroid-Team/enigma2]  (https://github.com/opendroid-Team/enigma2 "openDroid Enigma2")
> 

> and a lot more...


----------

# Building Instructions #

1 - Install packages on your buildserver

    sudo apt-get install -y autoconf automake bison bzip2 chrpath coreutils cvs default-jre default-jre-headless diffstat flex g++ gawk gcc gettext git-core gzip help2man htop info java-common libc6-dev libglib2.0-dev libperl4-corelibs-perl libproc-processtable-perl libtool libxml2-utils make ncdu ncurses-bin ncurses-dev patch perl pkg-config po4a python-setuptools quilt sgmltools-lite sshpass subversion swig tar texi2html texinfo wget xsltproc zip zlib1g-dev

----------
2 - Set your shell to /bin/bash.

    sudo dpkg-reconfigure dash
    When asked: Install dash as /bin/sh?
    select "NO"

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

    git clone git://github.com/oe-alliance/build-enviroment.git -b 3.4

----------
9 - Switch to folder build-enviroment

    cd build-enviroment

----------
10 - Update build-enviroment

    make update

----------
11 - Finally you can start building a image

    MACHINE=zgemmah2h DISTRO=opendroid make image
