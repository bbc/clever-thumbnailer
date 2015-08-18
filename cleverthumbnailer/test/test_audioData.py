from unittest import TestCase
from mock import patch, MagicMock

import numpy

from cleverthumbnailer import audiodata, ctexceptions

class TestAudioData(TestCase):
    # def test_waveData(self):
    #     self.fail()
    #
    # def test_sr(self):
    #     self.fail()

    def test_instantiate(self):
        x = audiodata.AudioData()
        self.assertEqual(x.loaded, False)

    @patch('wave.open')
    def test_loadFileMono(self, mockFile):
        mockWave = createMockAudio(1000, 2, 1, 44100)
        mockFile.return_value = mockWave

        x = audiodata.AudioData('test')
        self.assertEqual(x.byteDepth, 2)
        self.assertEqual(x.sr, 44100)
        self.assertEqual(x.loaded, True)
        self.assertEqual(len(x.waveData), 1000)

    @patch('wave.open')
    def test_loadFile2(self, mockFile):
        mockWave = createMockAudio(1000, 2, 2, 44100)
        mockFile.return_value = mockWave

        x = audiodata.AudioData('test')
        self.assertEqual(x.byteDepth, 2)
        self.assertEqual(x.sr, 44100)
        self.assertEqual(x.loaded, True)
        self.assertEqual(len(x.waveData), 1000)

    @patch('wave.open')
    def test_loadFileUnsupportedBitDepth(self, mockFile):
        mockWave = createMockAudio(1000, 3, 2, 44100)
        mockFile.return_value = mockWave

        with self.assertRaises(ctexceptions.FileFormatNotSupportedError):
            x = audiodata.AudioData('test')

    @patch('wave.open')
    def test_loadZeroSRFile(self, mockFile):
        mockWave = createMockAudio(1000, 3, 2, 0)
        mockFile.return_value = mockWave

        with self.assertRaises(ctexceptions.FileFormatNotSupportedError):
            x = audiodata.AudioData('test')

    @patch('wave.open')
    def test_loadZeroLengthFile(self, mockFile):
        # for a zero length file
        mockWave = createMockAudio(0, 2, 2, 44100)
        mockFile.return_value = mockWave
        x = audiodata.AudioData('test')
        self.assertEqual(len(x.waveData), 0)

    @patch('wave.open')
    def test_frames(self, mockFile):
        """Frames generates a stepped window of a certain length"""
        mockWave = createMockAudio(1000, 2, 2, 44100)
        mockFile.return_value = mockWave
        x = audiodata.AudioData(None)

    @patch('wave.open')
    def test_crop(self, mockFile):
        mockWave = createMockAudio(1000, 2, 2, 44100)
        mockFile.return_value = mockWave
        x = audiodata.AudioData('test')
        self.assertEqual(len(x.waveData),1000)
        x.crop(200,200)
        self.assertEqual(len(x.waveData),600)

    @patch('wave.open')
    def test_invalidCrop(self, mockFile):
        mockWave = createMockAudio(1000, 2, 2, 44100)
        mockFile.return_value = mockWave
        x = audiodata.AudioData('test')
        self.assertEqual(len(x.waveData),1000)
        x.crop(900.2,900)
        self.assertEqual(len(x.waveData),600)


def createMockAudio(length, byteDepth, channels, sr):
    """Create string of bytes ('0' character) for use in audio loading

    Args:
        length(int): length of string
        byteDepth(int): bit depth / 8 of audio
        channels(int): number of audio channels

    """
    mockWave = MagicMock()
    mockWave.getparams.return_value = (
        channels,  # number of channels
        byteDepth,  # byte depth (bitdepth/8)
        sr,  # sample rate
        length,  # length
        None, None)
    mockWave.readframes.return_value = '0' * length * byteDepth * channels
    return mockWave
        

