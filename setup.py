#!/usr/bin/env python
from setuptools import setup, Extension

setup(name="jellyfish",
      platforms=["any"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Text Processing :: Linguistic"],
      ext_modules=[Extension("jellyfish", ['jellyfishmodule.c', 'jaro.c',
                                        'hamming.c', 'levenshtein.c',
                                        'damerau_levenshtein.c', 'mra.c',
                                        'soundex.c', 'metaphone.c',
                                        'nysiis.c'])])
