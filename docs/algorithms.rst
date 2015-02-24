Algorithms
==========

Phonetic Encoding
~~~~~~~~~~~~~~~~~

These algorithms convert a string to a normalized phonetic encoding, converting a word to a
representation of its pronunciation.  Each algorithm takes a single string and returns a coded
representation.


soundex (American Soundex)
--------------------------

.. py:function:: jellyfish.soundex(s)

    Calculate the American Soundex of the string s.

Soundex is an algorithm to convert a word (typically a name) to a four digit code in the form 
'A123' where 'A' is the first letter of the name and the digits represent similar sounds.

For example ``soundex('Ann') == soundex('Anne') == 'A500'`` and
``soundex('Rupert') == soundex('Robert') == 'R163'``.

See the `Soundex article at Wikipedia <http://en.wikipedia.org/wiki/Soundex>`_ for more details.


metaphone
---------

.. py:function:: jellyfish.metaphone(s)

    Calculate the metaphone code for the string s.

The metaphone algorithm was designed as an improvement on Soundex.  It transforms a word into a
string consisting of '0BFHJKLMNPRSTWXY' where '0' is pronounced 'th' and 'X' is a '[sc]h' sound.

For example ``metaphone('Klump') == metaphone('Clump') == 'KLMP'``.

See the `Metaphone article at Wikipedia <http://en.wikipedia.org/wiki/Metaphone>`_ for more details.


nysiis
------

.. py:function:: jellyfish.nysiis(s)

    Calculate the NYSIIS code for the string s.

The NYSIIS algorithm is an algorithm developed by the New York State Identification and Intelligence System.  It transforms a word into a phonetic code.  Like soundex and metaphone it is primarily intended for use on names (as they would be pronounced in English).

For example ``nysiis('John') == nysiis('Jan') == JAN``.

See the `NYSIIS article at Wikipedia <http://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System>`_ for more details.

Match Rating Approach (codex)
-----------------------------

.. py:function:: jellyfish.match_rating_codex(s)

    Calculate the match rating approach (also called PNI) for the string s.

The Match rating approach algorithm is an algorithm for determining whether or not two names are
pronounced similarly.  The algorithm consists of an encoding function (similar to soundex or nysiis)
as well as a special comparison algorithm that can be used to compare names for equality using
the generated encoding.

See the `Match Rating Approach <http://en.wikipedia.org/wiki/Match_rating_approach>`_ for more details.

porter_stem
-----------

.. py:function:: jellyfish.porter_stem(s)

    Reduce the string s to its stem using the common Porter stemmer.

Stemming is the process of reducing a word to its root form, for example 'stemmed' to 'stem'.

Martin Porter's algorithm is a common algorithm used for stemming that works for many purposes.

See the `official homepage for the Porter Stemming Algorithm <http://tartarus.org/martin/PorterStemmer/>` for more details.
:
