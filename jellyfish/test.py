# -*- coding: utf-8 -*-
import csv
import unittest
import platform


class JellyfishTests(object):

    def test_jaro_winkler(self):
        cases = [("dixon", "dicksonx", 0.8133),
                 ("dixon", "dicksonx", 0.8133),
                 ("martha", "marhta", 0.9611),
                 ("dwayne", "duane", 0.84),
                 ]

        for (s1, s2, value) in cases:
            self.assertAlmostEqual(self.jf.jaro_winkler(s1, s2), value, places=4)

    def test_jaro_distance(self):
        cases = [("dixon", "dicksonx", 0.767),
                 ("dixon", "dicksonx", 0.767),
                 ("martha", "marhta", 0.944),
                 ("dwayne", "duane", 0.822),
                 ]

        for (s1, s2, value) in cases:
            self.assertAlmostEqual(self.jf.jaro_distance(s1, s2), value, places=3)

    def test_hamming_distance(self):
        cases = [("", "", 0),
                 ("", "abc", 3),
                 ("abc", "abc", 0),
                 ("acc", "abc", 1),
                 ("abcd", "abc", 1),
                 ("abc", "abcd", 1),
                 ("testing", "this is a test", 13),
                 ]

        for (s1, s2, value) in cases:
            self.assertEqual(self.jf.hamming_distance(s1, s2), value)

    def test_levenshtein_distance(self):
        cases = [("", "", 0),
                 ("abc", "", 3),
                 ("bc", "abc", 1),
                 ("kitten", "sitting", 3),
                 ("Saturday", "Sunday", 3),
                 ]

        for (s1, s2, value) in cases:
            self.assertEqual(self.jf.levenshtein_distance(s1, s2), value)

    def test_damerau_levenshtein_distance(self):
        cases = [("", "", 0),
                 ("abc", "", 3),
                 ("bc", "abc", 1),
                 ("abc", "acb", 1),
                 ]

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
        cases = [("metaphone", 'MTFN'),
                 ("wHErE", "WR"),
                 ("shell", "XL"),
                 ("this is a difficult string", "0S IS A TFKLT STRNK"),
                 ("aeromancy", "ERMNS"),
                 ("Antidisestablishmentarianism", "ANTTSSTBLXMNTRNSM"),
                 ("sunlight labs", "SNLT LBS"),
                 ("sonlite laabz", "SNLT LBS"),
                 (u"Çáŕẗéř", "KRTR"),
                 ('kentucky', 'KNTK'),
                 ('KENTUCKY', 'KNTK'),
                 ]

        for (s1, code) in cases:
            self.assertEqual(self.jf.metaphone(s1), code)

    def test_nysiis(self):
        cases = [("Worthy", "WARTY"),
                 ("Ogata", "OGAT"),
                 ("montgomery", "MANTGANARY"),
                 ("Costales", "CASTAL"),
                 ("Tu", "T"),
                 ("martincevic", "MARTANCAFAC"),
                 ("Catherine", "CATARAN"),
                 ("Katherine", "CATARAN"),
                 ("Katerina", "CATARAN"),
                 ("Johnathan", "JANATAN"),
                 ("Jonathan", "JANATAN"),
                 ("John", "JAN"),
                 ("Teresa", "TARAS"),
                 ("Theresa", "TARAS"),
                 ("Jessica", "JASAC"),
                 ("Joshua", "JAS"),
                 ("Bosch", "BAS"),
                 ("Lapher", "LAFAR"),
                 ]

        for (s1, s2) in cases:
            self.assertEqual(self.jf.nysiis(s1), s2)

    def test_match_rating_codex(self):
        cases = [("Byrne", "BYRN"),
                 ("Boern", "BRN"),
                 ("Smith", "SMTH"),
                 ("Smyth", "SMYTH"),
                 ("Catherine", "CTHRN"),
                 ("Kathryn", "KTHRYN"),
                 ]

        for (s1, s2) in cases:
            self.assertEqual(self.jf.match_rating_codex(s1), s2)

    def test_match_rating_comparison(self):
        cases = [("Bryne", "Boern", True),
                 ("Smith", "Smyth", True),
                 ("Catherine", "Kathryn", True),
                 ("Michael", "Mike", False),
                 ]

        for (s1, s2, value) in cases:
            self.assertEqual(self.jf.match_rating_comparison(s1, s2), value)

    def test_match_rating_comparison_segfault(self):
        import hashlib
        sha1s = [hashlib.sha1(str(v).encode('ascii')).hexdigest() for v in range(100)]
        # this segfaulted on 0.1.2
        assert [[self.jf.match_rating_comparison(h1, h2) for h1 in sha1s] for h2 in sha1s]

    def test_porter_stem(self):
        with open('porter-test.csv') as f:
            reader = csv.reader(f)
            for (a, b) in reader:
                self.assertEqual(self.jf.porter_stem(a.lower()), b.lower())


class PyJellyfishTestCase(unittest.TestCase, JellyfishTests):
    from . import _jellyfish as jf      # noqa


if platform.python_implementation() == 'CPython':
    class CJellyfishTestCase(unittest.TestCase, JellyfishTests):
        from . import cjellyfish as jf  # noqa


if __name__ == '__main__':
    unittest.main()
