#!/usr/bin/env python
import sys
from setuptools import setup, Extension, Command
from distutils.command.build_ext import build_ext
from distutils.errors import (CCompilerError, DistutilsExecError,
                               DistutilsPlatformError)

long_description = open('README.rst').read()

""" ripped off from simplejson's setup.py """
if sys.platform == 'win32' and sys.version_info > (2, 6):
   # 2.6's distutils.msvc9compiler can raise an IOError when failing to
   # find the compiler
   # It can also raise ValueError http://bugs.python.org/issue7511
   ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError,
                 IOError, ValueError)
else:
   ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)

IS_PYPY = hasattr(sys, 'pypy_translation_info')

class BuildFailed(Exception):
    pass

class ve_build_ext(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailed()


def run_setup(build_c):
    kw = {}

    if build_c:
        kw = dict(ext_modules=
                  [Extension("jellyfish.cjellyfish",
                             ['cjellyfish/jellyfishmodule.c',
                              'cjellyfish/jaro.c',
                              'cjellyfish/hamming.c',
                              'cjellyfish/levenshtein.c',
                              'cjellyfish/damerau_levenshtein.c',
                              'cjellyfish/mra.c',
                              'cjellyfish/soundex.c',
                              'cjellyfish/metaphone.c',
                              'cjellyfish/nysiis.c',
                              'cjellyfish/porter.c'])],
                  cmdclass=dict(build_ext=ve_build_ext)
                 )

    setup(name="jellyfish",
          version="0.3.0",
          platforms=["any"],
          description=("a library for doing approximate and "
                       "phonetic matching of strings."),
          url="http://github.com/sunlightlabs/jellyfish",
          long_description=long_description,
          classifiers=["Development Status :: 4 - Beta",
                       "Intended Audience :: Developers",
                       "License :: OSI Approved :: BSD License",
                       "Natural Language :: English",
                       "Operating System :: OS Independent",
                       "Programming Language :: Python",
                       "Topic :: Text Processing :: Linguistic"],
          **kw)

# run the setup func
try:
    run_setup(not IS_PYPY)
except BuildFailed:
    print('*'*75)
    print('WARNING: C extension could not be compiled, falling back to pure Python.')
    print('*'*75)
    run_setup(False)
    print('*'*75)
    print('WARNING: C extension could not be compiled, falling back to pure Python.')
    print('*'*75)

