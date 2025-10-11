# Overview

**jellyfish** is a library for approximate & phonetic matching of strings.

Source: <https://codeberg.org/jpt/jellyfish>

Documentation: <https://jellyfish.jpt.sh>

Issues: <https://codeberg.org/jpt/jellyfish/issues>

[![PyPI badge](https://badge.fury.io/py/jellyfish.svg)](https://badge.fury.io/py/jellyfish)

## Included Algorithms

String comparison:

* Levenshtein Distance
* Damerau-Levenshtein Distance
* Jaccard Index
* Jaro Distance
* Jaro-Winkler Distance
* Match Rating Approach Comparison
* Hamming Distance

Phonetic encoding:

* American Soundex
* Metaphone
* NYSIIS (New York State Identification and Intelligence System)
* Match Rating Codex

## Example Usage

``` python
>>> import jellyfish
>>> jellyfish.levenshtein_distance('jellyfish', 'smellyfish')
2
>>> jellyfish.jaro_similarity('jellyfish', 'smellyfish')
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
```
