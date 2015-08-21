import numpy
import logging
from collections import deque
import enum

from cleverthumbnailer.featureextractor.freqdomainextractor import \
    FrequencyDomainExtractor


class ApplauseState(enum.Enum):
    """Enum for tracking the diagnosed applause/music state of a track"""
    applause = 0
    music = 1


class ApplauseExtractor(FrequencyDomainExtractor):
    """Feature extractor that uses spectral centroid calculation and
    hysteresis to determine applause elements in an audio track.

    Applause detection works by:
        1) Calculating the spectral crest factor of a block of samples,
        and repeating at a preset interval across the entire audio file.
        2) Smoothing the resulting array using a moving average (top hat
        window for speed).
        3) Using thresholding and hysteresis to diagnose areas of applause and
        areas of music. Areas with low magnitude crest factor indicate low
        harmonic content, and are diagnosed as applause. Areas with high
        crest factor have higher harmonic content, and are diagnosed as music.
        4) Each change in state across the audio is stored as a (timestamp,
        diagnosis) tuple in a list of features (self.features).

    A helper method (ApplauseExtractor.checkApplause()) assists in diagnosing
    the state(applause/music) at a particular point in a song."""

    def __init__(self, sr, blockSize=1024, stepSize=512, threshold=0.04,
                 hysteresis=0.02, movingAverageLength=500):
        """
        Args:
            sr(int): sample rate of audio to be analysed
            blockSize(int): block size in samples for SCF calculation
            stepSize(int): step interval for SCF calculation
            threshold(float): threshold below which applause is diagnosed
            hysteresis(float): total amount of hysteresis centred around
                threshold
            movingAverageLength(int): number of previous SCF calculations to
            smooth result over.
        """
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
        """Calculate the mean of SCF moving average array"""
        # abstracted into seperate method to make it easier to use different
        # windowing functions in the future. Straight mean (top-hat window)
        # is computationally cheap.
        return numpy.mean(self.movingAverageBuffer)

    def processFrame(self, frame, timestamp):
        """Process one frame of signal according to frequency domain
        block input.

        Args:
            frame(Complex[]): frequency domain (FFT) frame. Should be of
                length self.blockSize
            timestamp(int): starting sample of block
        """
        assert len(frame) >= self.blockSize
        # obtain spectral crest factor for processed window
        spectralCrestFactor = spectralCrest(frame)
        # add SCF to buffer
        self.movingAverageBuffer.append(spectralCrestFactor)
        self._crestWave.append(spectralCrestFactor)
        bufferMean = self.calculateBufferMean()
        # see if we have a new feature (speech/music) for current buffer
        newState = self._applauseDetection(bufferMean)
        if newState is not None:
            # record state and time of new feature
            self._features.append((newState, timestamp))
            self._logger.debug(
                'New Event: {0} at time {1}'.format(newState, timestamp))

    def processRemaining(self):
        # all applause detection work is undertaken as we go along. Nothing to
        # do by the time this is called, but must be overridden so as not to
        # raise NotImplementedError()
        self._logger.debug('processRemaining() called but nothing to do.')
        pass

    def _applauseDetection(self, crestFactor):
        """Carry out music/applause diagnosis using history and latest frame

        Args:
            cfMagnitude(float): mean crest factor magnitude to diagnose
        Returns:
            ApplauseState: enum representing diagnosis.
        """

        # define lower and upper thresholds based on global threshold and
        # hysteresis levels
        lThresh = self.threshold - (self.hysteresis / 2.0)
        uThresh = self.threshold + (self.hysteresis / 2.0)

        # if we're currently in a 'music' state, use the lower threshold to
        # detect applause (enables hysteresis)
        if self._currentApplauseState is ApplauseState.music:
            if crestFactor < lThresh:
                # modify current state and return the new state
                self._currentApplauseState = ApplauseState.applause
                return self._currentApplauseState
        # if we're currently in an 'applause' state, use the upper threshold
        else:
            if crestFactor > uThresh:
                self._currentApplauseState = ApplauseState.music
                return self._currentApplauseState
        return None

    def getStateAtSample(self, sample):
        """Calculate and return the diagnosed applause/music state at a
        particular audio sample t

        Args:
            sample(int): The sample index at which state should be
            calculated

        Returns:
            ApplauseState: Either applause or music, according to
            ApplauseState enum."""
        position = numpy.searchsorted(
            [feature[0] for feature in self._features],
            sample, side='right') - 1
        if position < 0:
            # deals with the case that sample lands on or before first feature
            position = 0
        assert position >= 0
        assert position < len(self._features)
        return self._features[position], position

    def checkApplause(self, startSample, endSample):
        """Check to see if any occurrences of applause occur in a particular
        region
        Args:
            startSample(int): the start point of the region to check
            endSample(int): the end point of the region to check
        Returns:
            applauseOccurred(boolean): True if applause was detected
        """
        startIndex = self.getStateAtSample(startSample)[1]
        endIndex = self.getStateAtSample(endSample)[1]
        for feature in self._features[startIndex:endIndex]:
            featureType = feature[1]  # unbundle feature
            if featureType is ApplauseState.applause:
                return True
        return False

    @property
    def blockSize(self):
        return self._blockSize

    @property
    def stepSize(self):
        return self._stepSize


def spectralCrest(freqDomainFrame):
    """Calculate the crest factor of a block of audio
    Args:
        freqDomainFrame(complex array-like): freq domain info for audio block
    Returns:
        crestFactor(int): spectral crest factor of audio
    """
    magnitudeSpectrum = \
        numpy.absolute(freqDomainFrame) / (len(freqDomainFrame) * 0.5)
    totalSpectralPower = magnitudeSpectrum.sum()
    return magnitudeSpectrum.max() / totalSpectralPower  # crest
