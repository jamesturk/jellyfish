# -*- coding: utf-8 -*-
import unittest
import strfry


class StrfryTestCase(unittest.TestCase):

    def test_jaro_winkler(self):
        cases = [("dixon", "dicksonx", 0.8133),
                 ("dixon", "dicksonx", 0.8133),
                 ("martha", "marhta", 0.9611),
                 ("dwayne", "duane", 0.84),
                 ]

        for (s1, s2, value) in cases:
            self.assertAlmostEqual(strfry.jaro_winkler(s1, s2), value,
                                   places=4)


    def test_jaro_distance(self):
        cases = [("dixon", "dicksonx", 0.767),
                 ("dixon", "dicksonx", 0.767),
                 ("martha", "marhta", 0.944),
                 ("dwayne", "duane", 0.822),
                 ]

        for (s1, s2, value) in cases:
            self.assertAlmostEqual(strfry.jaro_distance(s1, s2), value,
                                   places=3)

    def test_hamming_distance(self):
        cases = [("", "", 0),
                 ("", "abc", 3),
                 ("abc", "aBc", 0),
                 ("acc", "abc", 1),
                 ("abcd", "abc", 1),
                 ("abc", "abcd", 1),
                 ("testing", "this is a test", 13),
                 ]

        for (s1, s2, value) in cases:
            self.assertEqual(strfry.hamming_distance(s1, s2), value)

    def test_hamming_distance_case_sensitive(self):
        cases = [("", "", 0),
                 ("", "abc", 3),
                 ("abc", "aBc", 1),
                 ("acc", "abc", 1),
                 ("abcd", "abc", 1),
                 ("abc", "Abcd", 2),
                 ("testing", "this is a test", 13),
                 ]

        for (s1, s2, value) in cases:
            self.assertEqual(strfry.hamming_distance(s1, s2, False), value)

    def test_levenshtein_distance(self):
        cases = [("", "", 0),
                 ("abc", "", 3),
                 ("bc", "abc", 1),
                 ("kitten", "sitting", 3),
                 ("Saturday", "Sunday", 3),
                 ]

        for (s1, s2, value) in cases:
            self.assertEqual(strfry.levenshtein_distance(s1, s2), value)

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
            self.assertEqual(strfry.soundex(s1), code)

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
                 ]

        for (s1, code) in cases:
            self.assertEqual(strfry.metaphone(s1), code)

if __name__ == '__main__':
    unittest.main()
