String Comparison
=================

These methods are all measures of the difference (aka `edit distance`) between two strings.

Levenshtein Distance
--------------------

.. py:function:: levenshtein_distance(s1, s2)

    Compute the Levenshtein distance between s1 and s2.

Levenshtein distance represents the number of insertions, deletions, and subsititutions required to change one word to another.

For example: ``levenshtein_distance('berne', 'born') == 2`` representing the transformation of the first e to o and the deletion of the second e.

See the `Levenshtein distance article at Wikipedia <http://en.wikipedia.org/wiki/Levenshtein_distance>`_ for more details.

Damerau-Levenshtein Distance
----------------------------

.. py:function:: damerau_levenshtein_distance(s1, s2)

    Compute the Damerau-Levenshtein distance between s1 and s2.

A modification of Levenshtein distance, Damerau-Levenshtein distance counts transpositions (such as ifhs for fish) as a single edit.

Where ``levenshtein_distance('fish', 'ifsh') == 2`` as it would require a deletion and an insertion,
though ``damerau_levenshtein_distance('fish', 'ifsh') == 1`` as this counts as a transposition.

See the `Damerau-Levenshtein distance article at Wikipedia <http://en.wikipedia.org/wiki/Damerau-Levenshtein_distance>`_ for more details.

Hamming Distance
----------------

.. py:function:: hamming_distance(s1, s2)

    Compute the Hamming distance between s1 and s2.

Hamming distance is the measure of the number of characters that differ between two strings.

Typically Hamming distance is undefined when strings are of different length, but this implementation
considers extra characters as differing.  For example ``hamming_distance('abc', 'abcd') == 1``.

See the `Hamming distance article at Wikipedia <http://en.wikipedia.org/wiki/Hamming_distance>`_ for more details.

Jaro Distance
-------------

.. py:function:: jaro_distance(s1, s2)

    Compute the Jaro distance between s1 and s2.

Jaro distance is a string-edit distance that gives a floating point response in [0,1] where 0 represents two completely dissimilar strings and 1 represents identical strings.

Jaro-Winkler Distance
---------------------

.. py:function:: jaro_winkler(s1, s2)

    Compute the Jaro-Winkler distance between s1 and s2.

Jaro-Winkler is a modification/improvement to Jaro distance, like Jaro it gives a floating point response in [0,1] where 0 represents two completely dissimilar strings and 1 represents identical strings.

See the `Jaro-Winkler distance article at Wikipedia <http://en.wikipedia.org/wiki/Jaro-Winkler_distance>`_ for more details.

Match Rating Approach (comparison)
----------------------------------

.. py:function:: match_rating_comparison(s1, s2)

    Compare s1 and s2 using the match rating approach algorithm, returns ``True`` if strings are considered equivalent or ``False`` if not.  Can also return ``None`` if s1 and s2 are not comparable (length differs by more than 3).

The Match rating approach algorithm is an algorithm for determining whether or not two names are
pronounced similarly.  Strings are first encoded using :py:func:`match_rating_codex` then compared according to the MRA algorithm.

See the `Match Rating Approach article at Wikipedia <http://en.wikipedia.org/wiki/Match_rating_approach>`_ for more details.
