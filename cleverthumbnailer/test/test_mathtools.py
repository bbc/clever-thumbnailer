from unittest import TestCase
from cleverthumbnailer.mathtools import coerceThumbnail
__author__ = 'jont'

class TestCoerceThumbnail(TestCase):
    def test_values(self):
        self.assertEquals(coerceThumbnail(0, 20, 40), (0, 20))
        self.assertEquals(coerceThumbnail(0, 40, 40), (0, 40))
        self.assertEquals(coerceThumbnail(10, 20, 40), (10, 20))
        self.assertEquals(coerceThumbnail(10, 30, 25), (5, 25))
        self.assertEquals(coerceThumbnail(-10, 10, 25), (0, 20))

    def test_assert(self):
        with self.assertRaises(AssertionError):
            coerceThumbnail(0, 40, 20)

    pass
