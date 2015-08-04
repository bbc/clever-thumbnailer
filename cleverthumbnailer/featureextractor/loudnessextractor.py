#!/usr/bin/env python
__author__ = 'Jon'

import numpy

from timedomainextractor import TimeDomainExtractor
from cleverthumbnailer.mathtools import interpMean, interpStats


class LoudnessExtractor(TimeDomainExtractor):
    """Process and store the windowed RMS of a signal.
    Attributes:
        sr (int): Working sample rate (in samples/sec) of feature extractor
        blockSize (int): Size of RMS window
        stepSize (int): Size of RMS step
        frameDomain (BlockDomain):
        features (np.array): Array of block RMS values.

    """

    def __init__(self, sr, blockSize=1024, stepSize=1024):
        super(LoudnessExtractor, self).__init__(sr)
        self._features = []
        self._currentsample = 0
        self._finishedVals = []
        self._blockSize = blockSize
        self._stepSize = stepSize

    @property
    def blockSize(self):
        return self._blockSize

    @property
    def stepSize(self):
        return self._blockSize

    def processFrame(self, frame, timestamp=None):
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

    def getStats(self, minSample, maxSample):
        return interpStats(self._features, minSample, maxSample)

    def getMeanInSeconds(self, minSeconds, maxSeconds):
        return interpMean(self._features, self.secsToSamples(minSeconds), self.secsToSamples(maxSeconds))


