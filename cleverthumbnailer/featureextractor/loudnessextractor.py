import numpy

from cleverthumbnailer.featureextractor import timedomainextractor
from cleverthumbnailer.utils import mathtools


class LoudnessExtractor(timedomainextractor.TimeDomainExtractor):
    """Find and store the windowed RMS amplitude of a signal.

    LoudnessExtractor.processAll() works by:
        1) Stepping through an audio waveform at a set interval (
        self.stepSize), processing a window of the next self.blockSize audio
        samples at each point.
        2) Storing each of these RMS values in a list (self.features),
        where each entry is a tuple of the form (timestampInSamples,
        rmsValueInVolts).

        Two helper methods, self.getMean() and self.getStats() are also
        provided

    Attributes:
        sr (int): Working sample rate (in samples/sec) of feature extractor
        blockSize (int): Size of RMS window
        stepSize (int): Interval in samples between RMS calculations
        frameDomain (BlockDomain):
        features (list): Array of block RMS values.

    """

    def __init__(self, sr, blockSize=1024, stepSize=1024):
        """
        Args:
            sr(int): Working sample rate (in samples/sec) of feature extractor
            blockSize(int): Size of RMS window for feature extractor
            stepSize(int): Interval in samples between RMS calculations
        """
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
        """Process a single frame/block of audio data with loudness algorithm.

        The loudness extractor algorithm does:
            1) finds the RMS energy of a single time-domain block
            2) Appends it to

        :param frame:
        :param timestamp:
        :return:
        """
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
        return mathtools.interpMean(self._features, minSample, maxSample)

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
        return mathtools.interpStats(self._features, minSample, maxSample)
