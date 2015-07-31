#!/usr/bin/env python
__author__ = 'Jon'

import enums

class GenericExtractor(object):
    """Base class for several audio feature extraction algorithms.

    Feature extractors process audio in small (typically 512-2048 big) blocks of time or frequency domain samples.
    Each block is processed iteratively and then the whole audio signal post-analysed once this has been completed.
    A feature extractor is configured at initialisation with (minimally) an audio sample rate.

    Attributes:
        sr (int): Working sample rate (in samples/sec) of feature extractor
        blockSize (int): Size of block or window to be processed
        stepSize (int): Size of expected step between iterated blocks
        frameDomain (BlockDomain): required domain of input signals (frequency or time)
        features (dict): features extracted so far
    """

    def __init__(self, sr):
        """
        Args:
            sr (int): required sample rate to work at
        Raises:
            TypeError: If `sr` is not a positive whole number
        """

        try:                                            # test for positive integer
            assert sr >= 0
            assert (sr*1.0).is_integer()
        except (TypeError, AssertionError, AttributeError):
            raise TypeError('Sample Rate sr must be a positive integer')

        # set attributes
        self.sr = sr
        self._features = None
        # set state
        self._done = False

    def processFrame(self, frame):
        """Process a single frame of input signal using feature extraction algorithm
        Args:
            frame (array-like): data for one audio frame for processing
        """
        raise NotImplementedError()

    def processRemaining(self):
        """Calculate any remaining audio features after processing each frame.

        Calling function will cause analysis to use information gathered from frames so far analysed. processRemaining()
        should usually be called after processing all audio frames using processFrames().
        """
        self._done = True

    @property
    def blockSize(self):
        raise NotImplementedError()

    @property
    def stepSize(self):
        raise NotImplementedError()

    @property
    def frameDomain(self):
        raise NotImplementedError()

    @property
    def features(self):
        return self._features

    def secsToSamples(self, secs):
        return secs*self.sr
