__author__ = 'jont'
from unittest import TestCase, main
from featureextractor import LoudnessExtractor
import numpy


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

    _MATHSTEST = [8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8]

    def test_CorrectLoudness(self):
        self.processLoudnessTest(0, 8, self._MATHSTEST, [(0,8), (8, 2), (16, 8)], 5)


    def processLoudnessTest(self, sr, blocksize, array, expectedFeatures, expectedMean, start=None, end=None):
        gen = LoudnessExtractor(sr)
        if not start:
            start = 0
        if not end:
            end = len(array)
        for fr in range(0, len(array), blocksize):
            testframe = array[fr:fr+blocksize]
            gen.processFrame(testframe)
        gen.processRemaining()
        f = gen.features
        self.assertEqual(gen.features, expectedFeatures)
        self.assertEqual(gen.getMean(start, end), expectedMean)

