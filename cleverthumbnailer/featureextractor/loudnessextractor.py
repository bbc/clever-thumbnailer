import numpy

from cleverthumbnailer.featureextractor.timedomainextractor import \
    TimeDomainExtractor
from cleverthumbnailer.utils.mathtools import interpMean, interpStats


class LoudnessExtractor(TimeDomainExtractor):
    """Process and store the windowed RMS of a signal.
    Attributes:
        sr (int): Working sample rate (in samples/sec) of feature extractor
        blockSize (int): Size of RMS window
        stepSize (int): Size of RMS step
        frameDomain (BlockDomain):
        features (list): Array of block RMS values.

    """

    def __init__(self, sr, blockSize=1024, stepSize=1024):
        super(LoudnessExtractor, self).__init__(sr)
        self._features = []
        self._currentSample = 0
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
        frameVals = numpy.asarray(frame)
        rms = numpy.sqrt(numpy.mean(numpy.square(frameVals)))
        # append tuple of current sample and RMS
        self._features.append((self._currentSample, rms))
        self._currentSample += len(frame)

    def processRemaining(self):
        self._done = True

    def getMean(self, minSample, maxSample):
        """Get the mean RMS value of a piece of audio

        Args:
            minSample: start time in samples
            maxSample: end time in samples

        Returns:
            mean (float): interpolated mean of audio extract RMS

        """
        return interpMean(self._features, minSample, maxSample)

    def getStats(self, minSample, maxSample):
        """Get the mean, min, and max RMS values of a piece of audio

        Args:
            minSample: start time in samples
            maxSample: end time in samples

        Returns:
            mean (float): interpolated mean of audio extract RMS
            min (float): minimum windowed RMS value of extract
            max (float): maximum windowed RMS value of extract

        """
        return interpStats(self._features, minSample, maxSample)
