#!/bin/bash
# https://github.com/pypa/python-manylinux-demo/blob/master/travis/build-wheels.sh

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w /io/wheelhouse/
    fi
}

# compile wheels
for PYBIN in /opt/python/cp3*/bin; do
  "${PYBIN}/pip" install /io/
  "${PYBIN}/pip" wheel /io/ --no-deps -w /io/wheelhouse/
done

# repair wheels
for whl in /io/wheelhouse/*.whl; do
    repair_wheel "$whl"
done

# copy testdata somewhere and test that the wheels work
cp -r /io/testdata/ $HOME
for PYBIN in /opt/python/cp3*/bin; do
  "${PYBIN}/pip" install pytest
  "${PYBIN}/pip" install jellyfish --no-index -f /io/wheelhouse
  (cd "$HOME"; "${PYBIN}/pytest" --pyargs jellyfish.test)
done
