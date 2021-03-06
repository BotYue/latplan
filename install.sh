#!/bin/bash
set -e

# errexit(){
#     echo $@ >&2
#     exit 1
# }

# if ! uname -a | grep Ubuntu ; then
#     echo "This is not ubuntu! Modify install.sh by yourself" >&2
# fi

sudo apt install -y mercurial g++ cmake make python flex bison g++-multilib
git submodule update --init --recursive
(
    hg clone http://hg.fast-downward.org downward
    cd downward
    ./build.py -j $(cat /proc/cpuinfo | grep -c processor) release64
)


# https://github.com/roswell/roswell/wiki/1.-Installation
sudo apt -y install git build-essential automake libcurl4-openssl-dev
git clone -b release https://github.com/roswell/roswell.git
(
    cd roswell
    sh bootstrap
    ./configure
    make
    sudo make install
    ros setup
)

ros install numcl/constantfold numcl/gtype numcl/specialized-function numcl/numcl
ros install guicho271828/magicffi guicho271828/dataloader guicho271828/remlic guicho271828/dsama
ros install arrival
ros install eazy-gnuplot

sudo apt install -y gnuplot

make -j 1 -C lisp

sudo apt -y install python3-pip python3-pil parallel \
     bash-completion byobu htop parallel mosh git
pip3 install --user \
     tensorflow keras h5py matplotlib progressbar2 \
     keras-adabound keras-rectified-adam \
     timeout_decorator ansicolors scipy scikit-image imageio
mkdir -p ~/.keras
cp keras-tf.json ~/.keras/keras.json

