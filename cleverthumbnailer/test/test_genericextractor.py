from unittest import TestCase, main

from cleverthumbnailer.featureextractor import GenericExtractor

class TestGenericExtractor(TestCase):
    def test_SR(self):
        self.assertRaises(TypeError, lambda _: GenericExtractor())
        self.assertRaises(TypeError, lambda _: GenericExtractor('string'))
        self.assertRaises(TypeError, lambda _: GenericExtractor(-1))
        self.assertRaises(TypeError, lambda _: GenericExtractor((2.1)))
        x = GenericExtractor(44100)
        self.assertEqual(x.sr, 44100)
        x.processRemaining()
        self.assertEqual(x.features, None) # should have no features

if __name__ == '__main__':
    main()
