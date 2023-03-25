# Functions

Jellyfish provides a variety of functions for string comparison, phonetic encoding, and stemming.

## String Comparison

These methods are all measures of the difference (aka edit distance) between two strings.

### Levenshtein Distance

``` python
def levenshtein_distance(s1: str, s2: str)
```

Compute the Levenshtein distance between s1 and s2.

Levenshtein distance represents the number of insertions, deletions, and substitutions required to change one word to another.

For example: ``levenshtein_distance('berne', 'born') == 2`` representing the transformation of the first e to o and the deletion of the second e.

See the [Levenshtein distance article at Wikipedia](http://en.wikipedia.org/wiki/Levenshtein_distance) for more details.

### Damerau-Levenshtein Distance

``` python
def damerau_levenshtein_distance(s1: str, s2: str)
```

Compute the Damerau-Levenshtein distance between s1 and s2.

A modification of Levenshtein distance, Damerau-Levenshtein distance counts transpositions (such as ifsh for fish) as a single edit.

Where ``levenshtein_distance('fish', 'ifsh') == 2`` as it would require a deletion and an insertion,
though ``damerau_levenshtein_distance('fish', 'ifsh') == 1`` as this counts as a transposition.

See the [Damerau-Levenshtein distance article at Wikipedia](http://en.wikipedia.org/wiki/Damerau-Levenshtein_distance) for more details.

### Hamming Distance

``` python
def hamming_distance(s1: str, s2: str)
```

Compute the Hamming distance between s1 and s2.

Hamming distance is the measure of the number of characters that differ between two strings.

Typically Hamming distance is undefined when strings are of different length, but this implementation
considers extra characters as differing.  For example ``hamming_distance('abc', 'abcd') == 1``.

See the [Hamming distance article at Wikipedia](http://en.wikipedia.org/wiki/Hamming_distance) for more details.

### Jaro Similarity

``` python
def jaro_similarity(s1: str, s2: str)
```

Compute the Jaro similarity between s1 and s2.

Jaro distance is a string-edit distance that gives a floating point response in [0,1] where 0 represents two completely dissimilar strings and 1 represents identical strings.

!!! warning

    Prior to 0.8.1 this function was named jaro_distance.  That name is still available, but is no longer recommended.
    It will be replaced in 1.0 with a correct version.

### Jaro-Winkler Similarity

``` python
def jaro_winkler_similarity(s1: str, s2: str)
```

Compute the Jaro-Winkler similarity between s1 and s2.

Jaro-Winkler is a modification/improvement to Jaro distance, like Jaro it gives a floating point response in [0,1] where 0 represents two completely dissimilar strings and 1 represents identical strings.

!!! warning

    Prior to 0.8.1 this function was named jaro_winkler.  That name is still available, but is no longer recommended.
    It will be replaced in 1.0 with a correct version.

See the [Jaro-Winkler distance article at Wikipedia](http://en.wikipedia.org/wiki/Jaro-Winkler_distance) for more details.

### Match Rating Approach (comparison)

``` python
def match_rating_comparison(s1, s2)
```

Compare s1 and s2 using the match rating approach algorithm, returns ``True`` if strings are considered equivalent or ``False`` if not.  Can also return ``None`` if s1 and s2 are not comparable (length differs by more than 3).

The Match rating approach algorithm is an algorithm for determining whether or not two names are
pronounced similarly.  Strings are first encoded using :py:func:`match_rating_codex` then compared according to the MRA algorithm.

See the [Match Rating Approach article at Wikipedia](http://en.wikipedia.org/wiki/Match_rating_approach) for more details.

## Phonetic Encoding

These algorithms convert a string to a normalized phonetic encoding, converting a word to a representation of its pronunciation.  Each takes a single string and returns a coded representation.


### American Soundex

``` python
def soundex(s: str)
```

Calculate the American Soundex of the string s.

Soundex is an algorithm to convert a word (typically a name) to a four digit code in the form 
'A123' where 'A' is the first letter of the name and the digits represent similar sounds.

For example ``soundex('Ann') == soundex('Anne') == 'A500'`` and
``soundex('Rupert') == soundex('Robert') == 'R163'``.

See the [Soundex article at Wikipedia](http://en.wikipedia.org/wiki/Soundex) for more details.


### Metaphone

``` python
def metaphone(s: str)
```

Calculate the metaphone code for the string s.

The metaphone algorithm was designed as an improvement on Soundex.  It transforms a word into a
string consisting of '0BFHJKLMNPRSTWXY' where '0' is pronounced 'th' and 'X' is a '[sc]h' sound.

For example ``metaphone('Klumpz') == metaphone('Clumps') == 'KLMPS'``.

See the [Metaphone article at Wikipedia](http://en.wikipedia.org/wiki/Metaphone) for more details.


### NYSIIS

``` python
def nysiis(s: str)
```

Calculate the NYSIIS code for the string s.

The NYSIIS algorithm is an algorithm developed by the New York State Identification and Intelligence System.  It transforms a word into a phonetic code.  Like soundex and metaphone it is primarily intended for use on names (as they would be pronounced in English).

For example ``nysiis('John') == nysiis('Jan') == JAN``.

See the [NYSIIS article at Wikipedia](http://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System) for more details.

### Match Rating Approach (codex)

``` python
def match_rating_codex(s: str)
```

Calculate the match rating approach value (also called PNI) for the string s.

The Match rating approach algorithm is an algorithm for determining whether or not two names are
pronounced similarly.  The algorithm consists of an encoding function (similar to soundex or nysiis)
which is implemented here as well as :py:func:`match_rating_comparison` which does the actual comparison.

See the [Match Rating Approach article at Wikipedia](http://en.wikipedia.org/wiki/Match_rating_approach) for more details.
