# Overview

**jellyfish** is a library for approximate & phonetic matching of strings.

Source: [https://codeberg.org/jpt/jellyfish](https://codeberg.org/jpt/jellyfish)

Documentation: [https://jamesturk.github.io/jellyfish/](https://jamesturk.github.io/jellyfish/)

Issues: [https://codeberg.org/jpt/jellyfish/issues](https://codeberg.org/jpt/jellyfish/issues)

[![PyPI badge](https://badge.fury.io/py/jellyfish.svg)](https://badge.fury.io/py/jellyfish)

## Included Algorithms

String comparison:

* Levenshtein Distance
* Damerau-Levenshtein Distance
* Jaccard Similarity
* Jaro Distance
* Jaro-Winkler Distance
* Match Rating Approach Comparison
* Hamming Distance

Phonetic encoding:

* American Soundex
* Metaphone
* NYSIIS (New York State Identification and Intelligence System)
* Match Rating Codex

## Implementations

Each algorithm has Rust and Python implementations.

The Rust implementations are used by default. The Python
implementations are a remnant of an early version of
the library and will probably be removed in 1.0.

To explicitly use a specific implementation, refer to the appropriate module::

``` python
import jellyfish._jellyfish as pyjellyfish
import jellyfish.rustyfish as rustyfish
```

If you've already imported jellyfish and are not sure what implementation you
are using, you can check by querying `jellyfish.library`.

``` python
  if jellyfish.library == 'Python':
      # Python implementation
  elif jellyfish.library == 'Rust':
      # Rust implementation
```

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
