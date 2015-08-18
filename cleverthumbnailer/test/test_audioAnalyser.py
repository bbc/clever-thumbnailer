from unittest import TestCase
from mock import patch, PropertyMock

from cleverthumbnailer.audioanalyser import AudioAnalyser


class TestAudioAnalyser(TestCase):

    @patch('cleverthumbnailer.audioanalyser.AudioData')
    def test_thumbLengthInSamples(self, audioData_mock):
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
