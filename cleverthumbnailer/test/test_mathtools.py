__author__ = 'Jon'
from unittest import main, TestCase
from cleverthumbnailer.mathtools import interpolate

class Test_interpolate(TestCase):
    def test_valids(self):
        earlyXY = (0, 1)
        lateXY = (1, 1)
        self.assertEqual(interpolate(earlyXY, lateXY, 0), 1)
        self.assertEqual(interpolate(earlyXY, lateXY, 0.5), 1)
        self.assertEqual(interpolate(earlyXY, lateXY, 0.8), 1)
        self.assertEqual(interpolate(earlyXY, lateXY, 1), 1)

    def test_invalid_interpolations(self):
        earlyXY = (0, 1)
        lateXY = (1, 1)
        self.assertRaises(ValueError, lambda _: interpolate(earlyXY, lateXY, -1))
        self.assertRaises(ValueError, lambda _: interpolate(earlyXY, lateXY, 2))
