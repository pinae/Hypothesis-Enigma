# -*- coding: utf-8 -*-
import unittest
import math
import sys
from hypothesis import given
from hypothesis.strategies import integers


def square(x: int) -> int:
    sq = x*x
    if sq > sys.maxsize:
        raise ArithmeticError("{0}*{0} is bigger than the maximum int.".format(x))
    return sq


def sqrt_rounded(x: int) -> int:
    return int(round(math.sqrt(x)))


class HypothesisPlaygroundTestCase(unittest.TestCase):
    @given(integers(min_value=0, max_value=3037000499))
    def test_square_and_sqrt(self, x):
        self.assertEqual(x, sqrt_rounded(square(x)))

    @given(integers(min_value=3037000500))
    def test_square_over_64_bit(self, x):
        self.assertRaises(ArithmeticError, square, x)
        try:
            square(x)
        except ArithmeticError as ex:
            self.assertEqual("{0}*{0} is bigger than the maximum int.".format(x), str(ex))


if __name__ == '__main__':  # pragma: no mutate
    unittest.main()  # pragma: no cover
