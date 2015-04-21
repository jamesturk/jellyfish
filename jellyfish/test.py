# -*- coding: utf-8 -*-
import sys
if sys.version_info[0] < 3:
    import unicodecsv as csv
else:
    import csv
import platform
import pytest


def assertAlmostEqual(a, b, places=3):
    assert abs(a - b) < (0.1**places)


if platform.python_implementation() == 'CPython':
    jf_params = ['python', 'c']
else:
    jf_params = ['python']


@pytest.fixture(params=jf_params)
def jf(request):
    if request.param == 'python':
        from jellyfish import _jellyfish as jf
    else:
        from jellyfish import cjellyfish as jf
    return jf


def test_jaro_winkler(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/jaro_winkler.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = float(value)
                assertAlmostEqual(jf.jaro_winkler(s1, s2), value, places=3)


def test_jaro_distance(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/jaro_distance.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = float(value)
                assertAlmostEqual(jf.jaro_distance(s1, s2), value, places=3)


def test_hamming_distance(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/hamming.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = int(value)
                assert jf.hamming_distance(s1, s2) == value


def test_levenshtein_distance(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/levenshtein.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = int(value)
                assert jf.levenshtein_distance(s1, s2) == value


def test_damerau_levenshtein_distance(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/damerau_levenshtein.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = int(value)
                assert jf.damerau_levenshtein_distance(s1, s2) == value


def test_soundex(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/soundex.csv') as f:
            data = csv.reader(f)
            for (s1, code) in data:
                assert jf.soundex(s1) == code


def test_metaphone(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/metaphone.csv') as f:
            data = csv.reader(f)
            for (s1, code) in data:
                assert jf.metaphone(s1) == code


def test_nysiis(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/nysiis.csv') as f:
            data = csv.reader(f)
            for (s1, s2) in data:
                assert jf.nysiis(s1) == s2


def test_match_rating_codex(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/match_rating_codex.csv') as f:
            data = csv.reader(f)
            for (s1, s2) in data:
                assert jf.match_rating_codex(s1) == s2


def test_match_rating_comparison(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/match_rating_comparison.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = {'True': True, 'False': False, 'None': None}[value]
                assert jf.match_rating_comparison(s1, s2) is value


def test_porter_stem(jf, benchmark):
    @benchmark
    def _():
        with open('testdata/porter.csv') as f:
            reader = csv.reader(f)
            for (a, b) in reader:
                assert jf.porter_stem(a) == b


if platform.python_implementation() == 'CPython':
    def test_match_rating_comparison_segfault():
        import hashlib
        from jellyfish import cjellyfish as jf
        sha1s = [hashlib.sha1(str(v).encode('ascii')).hexdigest() for v in range(100)]
        # this segfaulted on 0.1.2
        assert [[jf.match_rating_comparison(h1, h2) for h1 in sha1s] for h2 in sha1s]

    def test_damerau_levenshtein_distance_type():
        from jellyfish import cjellyfish as jf
        jf.damerau_levenshtein_distance(u'abc', u'abc')
        with pytest.raises(ValueError) as exc:
            jf.damerau_levenshtein_distance(b'abc', b'abc')
            assert 'expected' in str(exc.value)
