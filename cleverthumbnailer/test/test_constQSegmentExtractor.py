from unittest import TestCase
from featureextractor.constqsegmentextractor import ConstQSegmentExtractor
from audioanalyser import AudioData
__author__ = 'jont'
_TESTWAVE = '/home/jont/Dropbox/BBC2/Projects/Thumbnailer/Applause/jazzon3_thenecks_30s_1.wav'

class TestConstQSegmentExtractor(TestCase):
    audioData = None
    def setUp(self):
        self.audioData = AudioData(_TESTWAVE)

    def test_segmentSampleRate(self):
        self.fail()

    def test_nSegTypes(self):
        self.fail()

    def test_features(self):
        self.fail()

    def test_processFrame(self):
        self.fail()

    def test_processRemaining(self):
        self.fail()

    def test_frameDomain(self):
        self.fail()

    def test_blockSize(self):
        self.fail()

    def test_stepSize(self):
        self.fail()

    def test_makeParams(self):
        self.fail()

    # TODO: Set up mock tests to test individual modules
    def test_process(self):
        x = ConstQSegmentExtractor(self.audioData.sr)
        for frame in self.audioData.frames(x.stepSize, x.blockSize):
            x.processFrame(frame)
        x.processRemaining()
        for n, segment in enumerate(x.features):
            m1, s1 = divmod((segment.start/x.segmentSampleRate),60)  # time to minutes & seconds for readability
            m2, s2 = divmod((segment.end/x.segmentSampleRate),60)
            print('\tSection {0}: Type {1}. Start {2}m{3}s, end {4}m{5}s ({6} to {7} samples)'.format(
                n, segment.type, m1, s1, m2, s2, segment.start, segment.end))
        assert True

