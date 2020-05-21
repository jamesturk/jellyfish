#!/bin/bash
set -ex
export DOCKER_IMAGE=quay.io/pypa/manylinux2014_x86_64 
export PLAT=manylinux2014_x86_64
#docker run --rm -e PLAT=$PLAT -v `pwd`:/io $DOCKER_IMAGE /io/build-wheels.sh

python3 setup.py sdist
twine upload dist/* wheelhouse/*manylinux*

