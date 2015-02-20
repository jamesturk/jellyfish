# -*- coding: utf-8 -*-
import sys
if sys.version_info[0] < 3:
    import unicodecsv as csv
else:
    import csv
import unittest
import platform


class JellyfishTests(object):

    def test_jaro_winkler(self):
        with open('testdata/jaro_winkler.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = float(value)
                self.assertAlmostEqual(self.jf.jaro_winkler(s1, s2), value, places=3)

    def test_jaro_distance(self):
        with open('testdata/jaro_distance.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = float(value)
                self.assertAlmostEqual(self.jf.jaro_distance(s1, s2), value, places=3)

    def test_hamming_distance(self):
        with open('testdata/hamming.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = int(value)
                self.assertEqual(self.jf.hamming_distance(s1, s2), value)

    def test_levenshtein_distance(self):
        with open('testdata/levenshtein.csv') as f:
            data = csv.reader(f)
            for (s1, s2, value) in data:
                value = int(value)
                self.assertEqual(self.jf.levenshtein_distance(s1, s2), value)

    def test_damerau_levenshtein_distance(self):
        cases = [("", "", 0),
                 ("abc", "", 3),
                 ("bc", "abc", 1),
                 ("fuor", "four", 1),
                 ("abcd", "acb", 2),
                 ("cape sand recycling ", "edith ann graham", 17),
                 ("jellyifhs", "jellyfish", 2),
                 ("ifhs", "fish", 2),
                 ("Hello, world!", "Hello,\xc2\xa0world!", 2)]

        for (s1, s2, value) in cases:
            self.assertEqual(self.jf.damerau_levenshtein_distance(s1, s2), value)

    def test_soundex(self):
        cases = [("Washington", "W252"),
                 ("Lee", "L000"),
                 ("Gutierrez", "G362"),
                 ("Pfister", "P236"),
                 ("Jackson", "J250"),
                 ("Tymczak", "T522"),
                 ("", ""),
                 ("A", "A000"),
                 (u"Çáŕẗéř", "C636"),
                 ]

        for (s1, code) in cases:
            self.assertEqual(self.jf.soundex(s1), code)

    def test_metaphone(self):
        with open('testdata/metaphone.csv') as f:
            data = csv.reader(f)
            for (s1, code) in data:
                self.assertEqual(self.jf.metaphone(s1), code)

    def test_nysiis(self):
        with open('testdata/nysiis.csv') as f:
            data = csv.reader(f)
            for (s1, s2) in data:
                self.assertEqual(self.jf.nysiis(s1), s2)

    def test_match_rating_codex(self):
        with open('testdata/match_rating_codex.csv') as f:
            data = csv.reader(f)
            for (s1, s2) in data:
                self.assertEqual(self.jf.match_rating_codex(s1), s2)

    def test_match_rating_comparison(self):
        cases = [("Bryne", "Boern", True),
                 ("Smith", "Smyth", True),
                 ("Catherine", "Kathryn", True),
                 ("Michael", "Mike", False),
                 ("Tim", "Timothy", None),
                 ("Ed", "Ad", True),
                 ]

        for (s1, s2, value) in cases:
            self.assertEqual(self.jf.match_rating_comparison(s1, s2), value)

    def test_match_rating_comparison_segfault(self):
        import hashlib
        sha1s = [hashlib.sha1(str(v).encode('ascii')).hexdigest() for v in range(100)]
        # this segfaulted on 0.1.2
        assert [[self.jf.match_rating_comparison(h1, h2) for h1 in sha1s] for h2 in sha1s]

    def test_porter_stem(self):
        with open('testdata/porter.csv') as f:
            reader = csv.reader(f)
            for (a, b) in reader:
                self.assertEqual(self.jf.porter_stem(a.lower()), b.lower())


class PyJellyfishTestCase(unittest.TestCase, JellyfishTests):
    from jellyfish import _jellyfish as jf      # noqa


if platform.python_implementation() == 'CPython':
    class CJellyfishTestCase(unittest.TestCase, JellyfishTests):
        from jellyfish import cjellyfish as jf  # noqa


if __name__ == '__main__':
    unittest.main()
