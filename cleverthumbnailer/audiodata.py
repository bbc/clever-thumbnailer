# Copyright (C) 2015 British Broadcasting Corporation
#
# Cleverthumbnailer is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# Cleverthumbnailer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cleverthumbnailer; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import numpy
import wave
from cleverthumbnailer import ctexceptions
import logging

_logger = logging.getLogger(__name__)


class AudioData(object):
    """Container for low level mono audio information and IO.

    Attributes:
        waveData (list): mono-averaged audio samples from track
        sr (int): audio sample rate
        bitdepth (int): audio bit depth
    """

    def __init__(self, fileName=None):
        """Initialise and load audio if provided

        Args:
            fileName(string), optional: file to be loaded as AudioData object
        """
        self._wavefile = None
        self._sampleRate = None
        self._length = None
        self._waveData = None
        self.loaded = False
        self.byteDepth = None
        self.fileName = fileName
        self.offset = None
        if self.fileName:
            self.loadFile(fileName)
        pass

    @property
    def waveData(self):
        if self.loaded:
            return self._waveData
        raise ValueError('No file loaded')

    @property
    def sr(self):
        if self.loaded:
            return self._sampleRate
        raise ValueError('No file loaded')

    def crop(self, cropIn, cropOut):
        """Crops the audio file by a set number of samples"""
        self._waveData = self._waveData[cropIn:len(self.waveData)-cropOut]
        self.offset = cropIn


    def loadFile(self, filename):
        """Load audio file into AudioData object]

        Args:
            filename (str): Audio filename for loading

        Raises:
            FileFormatNotSupportedError: if the audio file loaded is not a
            16 or 24-bit WAVE file
            IOError: from the wave library if the file does not exist
        """
        self._wavefile = filename
        try:
            w = wave.open(filename, 'r')
            (nchannels, self.byteDepth, self._sampleRate, self._length,
             _, _) = w.getparams()
            if self.byteDepth == 1:
                origType = numpy.int8
            elif self.byteDepth == 2:
                origType = numpy.int16
            else:
                raise ctexceptions.FileFormatNotSupportedError(
                    '{0}-bit sample depth not supported'.format(
                        self.byteDepth * 8))
            wavType = numpy.dtype((origType, nchannels))
            multiChannelAudio = numpy.frombuffer(
                w.readframes(self._length), dtype=wavType)
            if numpy.ndim(multiChannelAudio) > 1:
                # mix down the multi channel audio into the mean of
                # each channel
                self._waveData = numpy.mean(
                    multiChannelAudio, 1) / numpy.iinfo(origType).max
            else:
                self._waveData = multiChannelAudio  # it is mono anyway

            assert len(multiChannelAudio) == self._length
            assert len(multiChannelAudio) == len(self._waveData)
            self.offset = 0
            self.loaded = True
        except wave.Error as e:
            eMessage = e.message if e.message else 'File could not be loaded'
            raise IOError(eMessage)

    def frames(self, stepSize, frameSize):
        """Generate sequential window based on known step and block size

        Args:
            stepSize (int): size of step between frames
            frameSize (int): size of window (or block) to be returned with
            each iteration

        Yields:
            list: audio frame of size frameSize
        """
        if not self.loaded:
            raise ValueError('No audio loaded to iterate over')

        assert (stepSize > 0)
        assert (self.waveData.ndim == 1)
        n = self.waveData.shape[0]
        print(n)
        i = 0
        while i < n:
            frame = self.waveData[i:i + frameSize]
            w = frame.shape[0]
            if w < frameSize:
                pad = numpy.zeros((frameSize - w))
                frame = numpy.concatenate((frame, pad), 1)
            yield frame.tolist()
            i += stepSize
