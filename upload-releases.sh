#!/bin/bash
set -ex

docker run --rm --privileged hypriot/qemu-register

function build_wheel() {
  ARCH=$1
  export DOCKER_IMAGE=quay.io/pypa/manylinux2014_$ARCH
  export PLAT=manylinux2014_$ARCH
  docker run --rm -e PLAT=$PLAT -v `pwd`:/io $DOCKER_IMAGE /io/build-wheels.sh
}

#Build wheels for x86_64
build_wheel "x86_64"

#Build wheels for aarch64
build_wheel "aarch64"

python3 setup.py sdist

twine upload dist/* wheelhouse/*manylinux*
