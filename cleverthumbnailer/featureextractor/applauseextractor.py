#!/usr/bin/env python
__author__ = 'Jon'

# Default Step size: 512
# Default Block size: 1024 (for 48khz)

import febase
import numpy
import enum
import logging
from collections import deque
from freqdomainextractor import FrequencyDomainExtractor

class ApplauseState(enum.Enum):
    applause = 0
    music = 1

class ApplauseExtractor(FrequencyDomainExtractor):
    def __init__(self, sr, blockSize=1024, stepSize=512, threshold=0.04, hysteresis=0.02, movingAverageLength=500):
        super(ApplauseExtractor, self).__init__(sr)
        self._logger = logging.getLogger(__name__)
        self._blockSize = blockSize
        self._stepSize = stepSize
        self._features = []
        self._crestWave = []
        self.threshold = threshold
        self.hysteresis = hysteresis
        self._currentApplauseState = None
        self.movingAverageBuffer = deque([], maxlen=movingAverageLength)

    def calculateBufferMean(self):
        return numpy.mean(self.movingAverageBuffer)

    @property
    def blockSize(self):
        return self._blockSize

    @property
    def stepSize(self):
        return self._stepSize

    def processFrame(self, frame, timestamp):
        """Process one frame of signal according to frequency domain block input.

        Args:
            frame(Complex[]): frequency domain (FFT) frame. Should be of length .blockSize
            timestamp(int): starting sample of block
        """
        assert len(frame) >= self.blockSize
        spectralCrestFactor = spectralCrest(frame)  # obtain spectral crest factor for processed window
        self.movingAverageBuffer.append(spectralCrestFactor)    # add SCF to buffer
        self._crestWave.append(spectralCrestFactor)
        bufferMean = self.calculateBufferMean()
        newState = self.applauseDetection(bufferMean)   # see if we have a new feature (speech/music) for current buffer
        if newState is not None:
            self._features.append((newState, timestamp)) # record state and time of new feature
            self._logger.debug('New Event: {0} at time {1}'.format(newState, timestamp))

    def processRemaining(self):
        self._logger.debug('processRemaining() called but nothing to do.')
        pass

    def applauseDetection(self, frame):
        threshold = self.threshold
        hysteresis = self.hysteresis
        lthresh = threshold-(hysteresis/2)
        uthresh = threshold+(hysteresis/2)

        if self._currentApplauseState is ApplauseState.music:
            if frame < lthresh:
                self._currentApplauseState = ApplauseState.applause
                return self._currentApplauseState
        else:
            if frame > uthresh:
                self._currentApplauseState = ApplauseState.music
                return self._currentApplauseState
        return None

def spectralCrest(freqDomainFrame):
    """Calculate the crest factory of a block of audio
    Args:
        freqDomainFrame(complex array-like): frequency domain information for audio block
    Returns:
        crestFactor(int): spectral crest factor of audio
    """
    magnitudeSpectrum = numpy.absolute(freqDomainFrame) / (len(freqDomainFrame)*0.5)
    totalSpectralPower = magnitudeSpectrum.sum()
    return magnitudeSpectrum.max() / totalSpectralPower    # crest