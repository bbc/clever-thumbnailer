#!/usr/bin/env python
__author__ = 'Jon'

from cleverthumbnailer.mathtools import interpolate
from unittest import TestCase, main

class TestInterpolate(TestCase):

    def test_flatLine(self):
        XY1 = (0, 1)
        XY2 = (1, 1)     # X1 < X2, Y1 = Y2 (values stay constant at unity over time)
        results = ((0, 1), (0.5, 1), (0.8, 1), (1, 1))
        self.checkInterpolate(XY1, XY2, results)

    def test_increaseLinear(self):
        XY1 = (0, 0)
        XY2 = (1, 1)     # X1 < X2, Y1 < Y2 (values increase linearly over time)
        results = ((0, 0), (0.5, 0.5), (0.8, 0.8), (1, 1))
        self.checkInterpolate(XY1, XY2, results)

    def test_validDecreasingWithDCOffset(self):
        XY1 = (0, 11)
        XY2 = (1, 10)     # X1 < X2, Y1 > Y2 (values decreasing over time and DC offset)
        results = ((0, 11), (0.5, 10.5), (0.8, 10.2), (1, 10))
        self.checkInterpolate(XY1, XY2, results)

    def test_validAndLarge(self):
        XY1 = (50000, 10000)
        XY2 = (100000, 20000)     # X1 < X2, Y1 < Y2 (X offset, large numbers)
        results = ((50000, 10000), (80000, 16000), (60000, 12000), (100000, 20000))
        self.checkInterpolate(XY1, XY2, results)

    def test_flippedCoefficients5(self):
        XY1 = (1, 1)
        XY2 = (0, 1)  # X1 > X2
        results = ((0, 1), (0.5, 1), (0.8, 1), (1, 1))
        self.checkInterpolate(XY1, XY2, results)

    def test_flippedAndDecreasing(self):
        XY1 = (1, 0)
        XY2 = (0, 1)  # X1 > X2, values increasing between 1 and 2 (so effectively decreasing)
        results = ((0, 1), (0.5, 0.5), (0.8, 0.2), (1, 0))
        self.checkInterpolate(XY1, XY2, results)

    def checkInterpolate(self, XY1, XY2, results):
        X1, X2 = XY1
        Y1, Y2 = XY2
        for inter, expected in results:
            self.assertAlmostEqual(interpolate(XY1, XY2, inter), expected,2)

if __name__ == '__main__':
    main()
