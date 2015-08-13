import numpy
import wave
import ctexceptions

class AudioData(object):
    """Container for low level mono audio information and IO.

    Attributes:
        waveData (list): mono-averaged audio samples from track
        sr (int): audio sample rate
        bitdepth (int): audio bit depth
    """

    def __init__(self, filename):
        self._wavefile = None
        self._sampleRate = None
        self._length = None
        self._waveData = None
        self.loaded = False
        self.bitDepth = None
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
        """Load audio file into AudioData object]

        Args:
            filename (str): Audio filename for loading

        Raises:
            FileFormatNotSupportedError: if the audio file loaded is not a
            16 or 24-bit WAVE file
        """
        self._wavefile = filename
        w = wave.open(filename, 'r')
        (nchannels, self.bitDepth, self._sampleRate, self._length,
         _, _) = w.getparams ()
        if self.bitDepth==1:
            origType = numpy.int8
        elif self.bitDepth==2:
            origType = numpy.int16
        else: raise ctexceptions.FileFormatNotSupportedError('{0}-bit sample depth not supported'.format(
            self.bitDepth*8))
        wavType = numpy.dtype((origType,nchannels))
        self.npOut = numpy.frombuffer(w.readframes(self._length), dtype=wavType)
        self._waveData = numpy.mean(self.npOut,1) / numpy.iinfo(origType).max
        self.loaded = True

    def frames(self, stepSize, frameSize):
        """Generate sequential window based on known step and block size

        Args:
            stepSize (int): size of step between frames
            frameSize (int): size of window (or block) to be returned with
            each iteration

        Yields:
            list: audio frame of size frameSize
        """
        assert(stepSize > 0)
        assert(self.waveData.ndim == 1)
        n = self.waveData.shape[0]
        print(n)
        i = 0
        while i < n:
            frame = self.waveData[i : i + frameSize]
            w = frame.shape[0]
            if w < frameSize:
                pad = numpy.zeros((frameSize - w))
                frame = numpy.concatenate((frame, pad), 1)
            yield frame.tolist()
            i = i + stepSize