#!/usr/bin/env python
"""Setup file for jellyfish."""

import os
import sys
from distutils.core import setup, Extension, Command
from distutils.command.build import build
from distutils import log

exts = [
    'jellyfishmodule.c', 'jaro.c', 'hamming.c', 'levenshtein.c',
    'damerau_levenshtein.c', 'mra.c', 'soundex.c', 'metaphone.c',
    'nysiis.c', 'porter.c']

class TestCommand(Command):
    """Command for running unittests without install."""

    user_options = [("args=", None, '''The command args string passed to
                                    unittest framework, such as 
                                     --args="-v -f"''')]

    def initialize_options(self):
        self.args = ''
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('build')
        bld = self.distribution.get_command_obj('build')
        #Add build_lib in to sys.path so that unittest can found DLLs and libs
        sys.path = [os.path.abspath(bld.build_lib)] + sys.path

        import shlex
        import unittest
        test_argv0 = [sys.argv[0] + ' test --args=']
        #For transfering args to unittest, we have to split args
        #by ourself, so that command like:
        #python setup.py test --args="-v -f"
        #can be executed, and the parameter '-v -f' can be
        #transfering to unittest properly.
        test_argv = test_argv0 + shlex.split(self.args)
        unittest.main(module=None, defaultTest='test.JellyfishTestCase', argv=test_argv)


cmdclass = {'test': TestCommand}

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Text Processing :: Linguistic"],

with open('README.rst') as readme:
    long_description = readme.read()

setup(name='jellyfish',
      version='0.2.1',
      platforms=['any'],
      description=("a library for doing approximate and "
                   "phonetic matching of strings."),
      url='http://github.com/sunlightlabs/jellyfish',
      long_description=long_description,
      classifiers=classifiers,
      license='BSD',
      ext_modules=[Extension('jellyfish', exts)],
      cmdclass=cmdclass)
