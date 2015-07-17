__author__ = 'Jon'

import qmsegmenter
from cleverthumbnailer.featureextractor import GenericExtractor, LoudnessExtractor
from unittest import TestCase, main
import numpy


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
        self.assertEqual(x.features, None)                      # should have no features


class TestLoudnessExtractor(TestCase):
    _TESTNOISE = [-0.60461333, -1.0398957 , -1.03974535, -2.03531057, -1.23099001,
                  -1.94003591, -0.99673211, -2.89883747,  1.09705007, -1.00000261,
                  -1.2865715 , -2.50027154, -1.23611381, -2.54326248, -1.23944335,
                  -2.93988439, -0.82125231,  2.58920872, -0.79654042, -2.22082306,
                  -0.76674609,  1.06854459, -1.42179897, -0.34839282,  0.92594817,
                  -0.5447573 , -1.57177398, -1.46559538, -1.53562477, -1.51038683,
                  -1.4750596 ,  0.13733937]

    _TESTSIN = [2.44929360e-16,   3.94355855e-01,   7.24792787e-01,
                9.37752132e-01,   9.98716507e-01,   8.97804540e-01,
                6.51372483e-01,   2.99363123e-01,  -1.01168322e-01,
                -4.85301963e-01,  -7.90775737e-01,  -9.68077119e-01,
                -9.88468324e-01,  -8.48644257e-01,  -5.71268215e-01,
                -2.01298520e-01,   2.01298520e-01,   5.71268215e-01,
                8.48644257e-01,   9.88468324e-01,   9.68077119e-01,
                7.90775737e-01,   4.85301963e-01,   1.01168322e-01,
                -2.99363123e-01,  -6.51372483e-01,  -8.97804540e-01,
                -9.98716507e-01,  -9.37752132e-01,  -7.24792787e-01,
                -3.94355855e-01,  -2.44929360e-16]

    _TESTDICT = {1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                 1.,  1.,  1.,  1.,  1.,  1.}

    def test_CorrectLoudness(self):
        t = numpy.linspace(-1,1,64)
        noise = numpy.random.normal(-1,1,100)    # should have
        sinwave = numpy.sin(t)
        gen = LoudnessExtractor(64, 8)
        for fr in range(0, len(sinwave), 8):
            testframe = sinwave[fr:fr+8]
            gen.processFrame(testframe)


if __name__ == '__main__':
    main()
