__author__ = 'Jon'

import qmsegmenter
from cleverthumbnailer.featureextractor import GenericExtractor, LoudnessExtractor
from unittest import TestCase, main


class TestGenericExtractor(TestCase):
    def test_SR(self):
        self.assertRaises(TypeError, lambda _: GenericExtractor())
        self.assertRaises(TypeError, lambda _: GenericExtractor('string'))
        self.assertRaises(TypeError, lambda _: GenericExtractor(-1))
        self.assertRaises(TypeError, lambda _: GenericExtractor((2.1)))
        x = GenericExtractor(44100)
        self.assertEqual(x.sr, 44100)
        self.assertRaises(ValueError, getattr, x, "features")   # property .features should throw ValueError
        x.processRemaining()

if __name__ == '__main__':
    main()