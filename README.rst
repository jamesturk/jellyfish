=========
jellyfish
=========

Jellyfish is a python library for doing approximate and phonetic matching of strings.

jellyfish is a project of Sunlight Labs (c) 2010.
All code is released under a BSD-style license, see LICENSE for details.

Written by Michael Stephens <mstephens@sunlightfoundation.com> and James Turk
<jturk@sunlightfoundation.com>.

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