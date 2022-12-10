import unittest
from solution import distance


class Tests(unittest.TestCase):

    def test_distance(self):
        cases = [
            (("abcde", "bcd"), 2),
            (("abcde", "abcde"), 0),
            (("cde", "abcde"), 2),
            (("", "abcd"), -1),
            (("abc", "cde"), 4)
        ]
        for i, ((a, b), expected) in enumerate(cases):
            with self.subTest(i=i):
                actual = distance(a, b)
                self.assertEqual(expected, actual)
