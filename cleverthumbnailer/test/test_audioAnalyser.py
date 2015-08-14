from unittest import TestCase
from audioanalyser import AudioAnalyser
from mock import MagicMock, patch, PropertyMock
__author__ = 'jont'


class TestAudioAnalyser(TestCase):
    def test_loadAudio(self):
        # test for: 1) That a valid audio file loads. 2) That we get an
        # exception for an invalid file

        # we should only test the loadAudio procedure itself (not the
        # AudioData instantiator method)
        self.fail()

    @patch('cleverthumbnailer.audioanalyser.AudioData')
    def test_thumbLengthInSamples(self, audioData_mock):
        # test for: 1) a valid calculation, 2) what happens when sample rate
        #  is set to something stupid

        audioData_mock.return_value.sr = PropertyMock(return_value=44100)


        x = AudioAnalyser()
        x.loadAudio('test.wav')
        self.assertEquals(x.inSamples(10), 441000)

    def test_thumbnail(self):
        self.fail()

    def test_processAll(self):


        self.fail()

    def test__pickThumbnail(self):
        self.fail()

    def test_middleThumbNail(self):
        self.fail()

    def test_inSeconds(self):
        self.fail()

    def test_inSamples(self):
        self.fail()
