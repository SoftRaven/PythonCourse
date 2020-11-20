import unittest
from SimpleNumbersGenerator import *


class TestSimpleNumbersGenerator(unittest.TestCase):

    def setUp(self):
        self.sng = SimpleNumbersGenerator()

    def test_case_ceil_10(self):
        ceil = 10
        expected = [2, 3, 5, 7]

        result = self.sng.generate(ceil)

        self.assertEqual(expected, result)

    def test_case_ceil_20(self):
        ceil = 20
        expected = [2, 3, 5, 7, 11, 13, 17, 19]

        result = self.sng.generate(ceil)

        self.assertEqual(expected, result)

    def test_case_ceil_100(self):
        ceil = 100
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

        result = self.sng.generate(ceil)

        self.assertEqual(expected, result)

    def test_case_negative_ceil(self):
        ceil = -20
        expected = ValueError

        result = self.sng.generate

        with self.assertRaises(expected):
            result(ceil)

    def test_case_zero_ceil(self):
        ceil = 0
        expected = []

        result = self.sng.generate(ceil)

        self.assertEqual(expected, result)
