=========
jellyfish
=========

.. image:: https://travis-ci.org/sunlightlabs/jellyfish.svg?branch=master
    :target: https://travis-ci.org/sunlightlabs/jellyfish

.. image:: https://coveralls.io/repos/sunlightlabs/jellyfish/badge.png?branch=master
    :target: https://coveralls.io/r/sunlightlabs/jellyfish

.. image:: https://pypip.in/version/jellyfish/badge.svg
    :target: https://pypi.python.org/pypi/jellyfish

.. image:: https://pypip.in/format/jellyfish/badge.svg
    :target: https://pypi.python.org/pypi/jellyfish

.. image:: https://readthedocs.org/projects/jellyfish/badge/?version=latest
    :target: https://readthedocs.org/projects/jellyfish/?badge=latest
    :alt: Documentation Status

.. image:: https://ci.appveyor.com/api/projects/status/github/sunlightlabs/jellyfish?branch=master&svg=true
    :target: https://ci.appveyor.com/project/jamesturk/jellyfish/


Jellyfish is a python library for doing approximate and phonetic matching of strings.

jellyfish is a project of Sunlight Labs (c) 2014.
All code is released under a BSD-style license, see LICENSE for details.

Written by James Turk <jturk@sunlightfoundation.com> and Michael Stephens.

See https://github.com/sunlightlabs/jellyfish/graphs/contributors for contributors.

Source is available at http://github.com/sunlightlabs/jellyfish.

Included Algorithms
===================

String comparison:

  * Levenshtein Distance
  * Damerau-Levenshtein Distance
  * Jaro Distance
  * Jaro-Winkler Distance
  * Match Rating Approach Comparison
  * Hamming Distance

Phonetic encoding:

  * American Soundex
  * Metaphone
  * NYSIIS (New York State Identification and Intelligence System)
  * Match Rating Codex

Example Usage
=============

>>> import jellyfish
>>> jellyfish.levenshtein_distance('jellyfish', 'smellyfish')
2
>>> jellyfish.jaro_distance('jellyfish', 'smellyfish')
0.89629629629629637
>>> jellyfish.damerau_levenshtein_distance('jellyfish', 'jellyfihs')
1

>>> jellyfish.metaphone('Jellyfish')
'JLFX'
>>> jellyfish.soundex('Jellyfish')
'J412'
>>> jellyfish.nysiis('Jellyfish')
'JALYF'
>>> jellyfish.match_rating_codex('Jellyfish')
'JLLFSH'
