from hypothesis import given, settings, Verbosity
from hypothesis.strategies import text

import jellyfish.cjellyfish as cjellyfish
import jellyfish._jellyfish as pyjellyfish


@given(text())
def test_py_soundex_equals_c_soundex(s):
    py_soundex = pyjellyfish.soundex(s)
    c_soundex = cjellyfish.soundex(s)
    assert py_soundex == c_soundex


@given(text())
def test_py_nysiis_equals_c_nysiis(s):
    py_nysiis = pyjellyfish.nysiis(s)
    c_nysiis = cjellyfish.nysiis(s)
    assert py_nysiis == c_nysiis


@given(text())
def test_py_match_rating_codex_equals_c_match_rating_codex(s):
    py_match_rating_codex = pyjellyfish.match_rating_codex(s)
    c_match_rating_codex = cjellyfish.match_rating_codex(s)
    assert py_match_rating_codex == c_match_rating_codex


@given(text())
def test_py_metaphone_equals_c_metaphone(s):
    py_metaphone = pyjellyfish.metaphone(s)
    c_metaphone = cjellyfish.metaphone(s)
    assert py_metaphone == c_metaphone


@given(text())
def test_py_porter_stem_equals_c_porter_stem(s):
    py_porter_stem = pyjellyfish.porter_stem(s)
    c_porter_stem = cjellyfish.porter_stem(s)
    assert py_porter_stem == c_porter_stem


@given(s1=text(), s2=text())
def test_py_levenshtein_distance_equals_c_levenshtein_distance(s1, s2):
    py_levenshtein_distance = pyjellyfish.levenshtein_distance(s1, s2)
    c_levenshtein_distance = cjellyfish.levenshtein_distance(s1, s2)
    assert py_levenshtein_distance == c_levenshtein_distance


@given(s1=text(), s2=text())
def test_py_damerau_levenshtein_distance_equals_c_damerau_levenshtein_distance(s1, s2):
    py_damerau_levenshtein_distance = pyjellyfish.damerau_levenshtein_distance(s1, s2)
    c_damerau_levenshtein_distance = cjellyfish.damerau_levenshtein_distance(s1, s2)
    assert py_damerau_levenshtein_distance == c_damerau_levenshtein_distance


@given(s1=text(), s2=text())
def test_py_hamming_distance_equals_c_hamming_distance(s1, s2):
    py_hamming_distance = pyjellyfish.hamming_distance(s1, s2)
    c_hamming_distance = cjellyfish.hamming_distance(s1, s2)
    assert py_hamming_distance == c_hamming_distance


@given(s1=text(), s2=text())
def test_py_jaro_distance_equals_c_jaro_distance(s1, s2):
    py_jaro_distance = pyjellyfish.jaro_distance(s1, s2)
    c_jaro_distance = cjellyfish.jaro_distance(s1, s2)
    assert py_jaro_distance == c_jaro_distance


@given(s1=text(), s2=text())
def test_py_jaro_winkler_equals_c_jaro_winkler(s1, s2):
    py_jaro_winkler = pyjellyfish.jaro_winkler(s1, s2)
    c_jaro_winkler = cjellyfish.jaro_winkler(s1, s2)
    assert py_jaro_winkler == c_jaro_winkler


@given(s1=text(), s2=text())
@settings(verbosity=Verbosity.verbose)
def test_py_match_rating_comparison_equals_c_match_rating_comparison(s1, s2):
    py_match_rating_comparison = pyjellyfish.match_rating_comparison(s1, s2)
    c_match_rating_comparison = cjellyfish.match_rating_comparison(s1, s2)
    assert py_match_rating_comparison == c_match_rating_comparison
