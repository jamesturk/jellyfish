#!/usr/bin/env python
from setuptools import setup, Extension

setup(name="strfry",
      platforms=["any"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Text Processing :: Linguistic"],
      ext_modules=[Extension("strfry", ['strfrymodule.c', 'jaro.c',
                                        'hamming.c', 'levenshtein.c',
                                        'soundex.c', 'metaphone.c'])])
