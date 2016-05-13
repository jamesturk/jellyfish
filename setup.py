#!/usr/bin/env python
import os
import sys
from setuptools import setup, Extension, Command
from distutils.command.build_ext import build_ext
from distutils.errors import (CCompilerError, DistutilsExecError, DistutilsPlatformError)

# large portions ripped off from simplejson's setup.py

if sys.platform == 'win32' and sys.version_info > (2, 6):
    # 2.6's distutils.msvc9compiler can raise an IOError when failing to find the compiler
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


class TestCommand(Command):
    """Command for running unittests without install."""

    user_options = [("args=", None, '''The command args string passed to
                                    unittest framework, such as --args="-v -f"''')]

    def initialize_options(self):
        self.args = ''
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('build')
        bld = self.distribution.get_command_obj('build')
        # Add build_lib in to sys.path so that unittest can found DLLs and libs
        sys.path = [os.path.abspath(bld.build_lib)] + sys.path

        import shlex
        import unittest
        test_argv0 = [sys.argv[0] + ' test --args=']
        # For transferring args to unittest, we have to split args
        # by ourself, so that command like:
        # python setup.py test --args="-v -f"
        # can be executed, and the parameter '-v -f' can be
        # transferring to unittest properly.
        test_argv = test_argv0 + shlex.split(self.args)
        unittest.main(module='jellyfish.test', argv=test_argv)


def run_setup(build_c):
    kw = {}

    if build_c:
        kw = dict(
            ext_modules=[Extension("jellyfish.cjellyfish",
                                   ['cjellyfish/jellyfishmodule.c',
                                    'cjellyfish/jaro.c',
                                    'cjellyfish/hamming.c',
                                    'cjellyfish/levenshtein.c',
                                    'cjellyfish/damerau_levenshtein.c',
                                    'cjellyfish/mra.c',
                                    'cjellyfish/soundex.c',
                                    'cjellyfish/metaphone.c',
                                    'cjellyfish/nysiis.c',
                                    'cjellyfish/porter.c'],
                                   define_macros=[('CJELLYFISH_PYTHON', '1')],
                                   )],
            cmdclass=dict(build_ext=ve_build_ext, test=TestCommand),
            packages=['jellyfish'],
        )
    else:
        kw = dict(cmdclass=dict(test=TestCommand), packages=['jellyfish'])

    with open('README.rst') as readme:
        long_description = readme.read()

    setup(name="jellyfish",
          version="0.5.4",
          platforms=["any"],
          description=("a library for doing approximate and "
                       "phonetic matching of strings."),
          url="http://github.com/jamesturk/jellyfish",
          long_description=long_description,
          classifiers=["Development Status :: 4 - Beta",
                       "Intended Audience :: Developers",
                       "License :: OSI Approved :: BSD License",
                       "Natural Language :: English",
                       "Operating System :: OS Independent",
                       "Programming Language :: Python :: 2.7",
                       "Programming Language :: Python :: 3.3",
                       "Programming Language :: Python :: 3.4",
                       "Topic :: Text Processing :: Linguistic"],
          **kw)

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
