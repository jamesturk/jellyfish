Phonetic Encoding
=================

These algorithms convert a string to a normalized phonetic encoding, converting a word to a representation of its pronunciation.  Each takes a single string and returns a coded representation.


American Soundex
----------------

``` python
def soundex(s: str)
```

Calculate the American Soundex of the string s.

Soundex is an algorithm to convert a word (typically a name) to a four digit code in the form 
'A123' where 'A' is the first letter of the name and the digits represent similar sounds.

For example ``soundex('Ann') == soundex('Anne') == 'A500'`` and
``soundex('Rupert') == soundex('Robert') == 'R163'``.

See the [Soundex article at Wikipedia](http://en.wikipedia.org/wiki/Soundex) for more details.


Metaphone
---------

``` python
def metaphone(s: str)
```

Calculate the metaphone code for the string s.

The metaphone algorithm was designed as an improvement on Soundex.  It transforms a word into a
string consisting of '0BFHJKLMNPRSTWXY' where '0' is pronounced 'th' and 'X' is a '[sc]h' sound.

For example ``metaphone('Klumpz') == metaphone('Clumps') == 'KLMPS'``.

See the [Metaphone article at Wikipedia](http://en.wikipedia.org/wiki/Metaphone) for more details.


NYSIIS
------

``` python
def nysiis(s: str)
```

Calculate the NYSIIS code for the string s.

The NYSIIS algorithm is an algorithm developed by the New York State Identification and Intelligence System.  It transforms a word into a phonetic code.  Like soundex and metaphone it is primarily intended for use on names (as they would be pronounced in English).

For example ``nysiis('John') == nysiis('Jan') == JAN``.

See the [NYSIIS article at Wikipedia](http://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System) for more details.

Match Rating Approach (codex)
-----------------------------

``` python
def match_rating_codex(s: str)
```

Calculate the match rating approach value (also called PNI) for the string s.

The Match rating approach algorithm is an algorithm for determining whether or not two names are
pronounced similarly.  The algorithm consists of an encoding function (similar to soundex or nysiis)
which is implemented here as well as :py:func:`match_rating_comparison` which does the actual comparison.

See the [Match Rating Approach article at Wikipedia](http://en.wikipedia.org/wiki/Match_rating_approach) for more details.
