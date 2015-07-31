#!/usr/bin/env python
__author__ = 'Jon'

import febase
import numpy
import enums
from cleverthumbnailer.mathtools import interpMean

class LoudnessExtractor(febase.GenericExtractor):
    """Process and store the windowed RMS of a signal.
    Attributes:
        sr (int): Working sample rate (in samples/sec) of feature extractor
        blockSize (int): Size of RMS window
        stepSize (int): Size of RMS step
        frameDomain (BlockDomain):
        features (np.array): Array of block RMS values.

    """

    def __init__(self, sr):
        super(LoudnessExtractor, self).__init__(sr)
        self._features = []
        self._currentsample = 0
        self._finishedVals = []

    @property
    def blockSize(self):
        return self._blockSize

    @property
    def stepSize(self):
        return self._blockSize

    def frameDomain(self):
        return enums.BlockDomain.time       # Time domain extractor

    def processFrame(self, frame):
        # don't worry about frame size; just process anyway
        framevals = numpy.asarray(frame)
        rms = numpy.sqrt(numpy.mean(numpy.square(framevals)))
        self._features.append((self._currentsample, rms))   # append tuple of current sample and RMS
        self._currentsample += len(frame) #

    def processRemaining(self):
        self._done = True

    def getMean(self, minSample, maxSample):
        # get mean windowed RMS between min and max samples
        return interpMean(self._features, minSample, maxSample)

    def getMeanInSeconds(self, minSeconds, maxSeconds):
        return interpMean(self._features, self.secsToSamples(minSeconds), self.secsToSamples(maxSeconds))


