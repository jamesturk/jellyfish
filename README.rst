=========
jellyfish
=========

.. image:: https://travis-ci.org/jamesturk/jellyfish.svg?branch=master
    :target: https://travis-ci.org/jamesturk/jellyfish

.. image:: https://coveralls.io/repos/jamesturk/jellyfish/badge.png?branch=master
    :target: https://coveralls.io/r/jamesturk/jellyfish

.. image:: https://img.shields.io/pypi/v/jellyfish.svg
    :target: https://pypi.python.org/pypi/jellyfish

.. image:: https://readthedocs.org/projects/jellyfish/badge/?version=latest
    :target: https://readthedocs.org/projects/jellyfish/?badge=latest
    :alt: Documentation Status

.. image:: https://ci.appveyor.com/api/projects/status/t5o03rqcusxhhe41/branch/master?svg=true
    :target: https://ci.appveyor.com/project/jamesturk/jellyfish/

Jellyfish is a python library for doing approximate and phonetic matching of strings.

Written by James Turk <james.p.turk@gmail.com> and Michael Stephens.

See https://github.com/jamesturk/jellyfish/graphs/contributors for contributors.

Source is available at http://github.com/jamesturk/jellyfish.

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
>>> jellyfish.levenshtein_distance(u'jellyfish', u'smellyfish')
2
>>> jellyfish.jaro_distance(u'jellyfish', u'smellyfish')
0.89629629629629637
>>> jellyfish.damerau_levenshtein_distance(u'jellyfish', u'jellyfihs')
1

>>> jellyfish.metaphone(u'Jellyfish')
'JLFX'
>>> jellyfish.soundex(u'Jellyfish')
'J412'
>>> jellyfish.nysiis(u'Jellyfish')
'JALYF'
>>> jellyfish.match_rating_codex(u'Jellyfish')
'JLLFSH'
