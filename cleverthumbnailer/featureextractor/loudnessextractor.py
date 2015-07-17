#!/usr/bin/env python
__author__ = 'Jon'

import febase


class LoudnessExtractor(febase.GenericExtractor):
    """Process and store the windowed RMS of a signal.
    Attributes:
        sr (int): Working sample rate (in samples/sec) of feature extractor
        blockSize (int): Size of RMS window
        stepSize (int): Size of RMS step
        frameDomain (BlockDomain):
        features (np.array): Array of block RMS values.

    """

    def __init__(self, sr, blockSize=1024):
        super(LoudnessExtractor, self).__init__(sr)
        self._blockSize = blockSize
        self._features = numpy.array([])

    @property
    def blockSize(self):
        return self._blockSize

    @property
    def stepSize(self):
        return self._blockSize

    def processFrame(self, frame):
        if len(frame) != self._blockSize:
            raise ValueError('Frame length is not correct for given block size ({0})'.format(self._blockSize))
        framevals = numpy.asarray(frame)
        rms = numpy.sqrt(numpy.mean(numpy.square(framevals)))
        self._features.append(rms)

    def processRemaining(self):
        self._done = True