__author__ = 'jont'

import numpy
import wave

class AudioData(object):
    def __init__(self, filename):
        self._wavefile = None
        self._bytesPerSample = None
        self._sampleRate = None
        self._length = None
        self._waveData = None
        self.comptype = None
        self.loaded = False

        self.loadFile(filename)
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

    def loadFile(self, filename):
        self._wavefile = filename
        w = wave.open(filename, 'r')
        (nchannels, self._bytesPerSample, self._sampleRate, self._length, comptype, compname) = w.getparams ()
        if self._bytesPerSample==1:
            origType = numpy.int8
        elif self._bytesPerSample==2:
            origType = numpy.int16
        else: raise ValueError('{0}-bit sample depth not supported'.format(self._bytesPerSample*8))
        wavType = numpy.dtype((origType,nchannels))
        self.npOut = numpy.frombuffer(w.readframes(self._length), dtype=wavType)
        self._waveData = numpy.mean(self.npOut,1) / numpy.iinfo(origType).max
        self.loaded = True

    def frames(self, step_size, frame_size):
        """
        Take step and frame size, and return iterator over audio data for processing in blocks.
        """
        assert(step_size > 0)
        assert(self.waveData.ndim == 1)
        n = self.waveData.shape[0]
        print(n)
        i = 0
        while i < n:
            frame = self.waveData[i : i + frame_size]
            w = frame.shape[0]
            if w < frame_size:
                pad = numpy.zeros((frame_size - w))
                frame = numpy.concatenate((frame, pad), 1)
            yield frame.tolist()
            i = i + step_size