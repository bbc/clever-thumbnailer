#!/usr/bin/env python
"""Audio feature extraction classes for use with BBC audio thumbnail chooser application"""

import enum
import qmsegmenter
import numpy

class BlockDomain(enum.Enum):
    """Enum for expected feature extractor domain."""
    time = 1
    frequency = 2

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
            assert self.sr > 0
            assert self.sr.is_integer()
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
        if not self._done:                              # raise exception if we haven't performed any analysis yet
            raise  ValueError('Audio features not yet been extracted')
        return self._features


class ConstQSegmentExtractor(GenericExtractor):
    """Wrapper for QM DSP Constant-Q Segmenter_ algorithm.

    Analyzes audio and creates a candidate set of musical sections, described by type and timestamp. Such sections
    may resemble 'chorus', 'bridge', 'verse', and are calculated based on musical similarity metrics.

    _Segmenter: https://code.soundsoftware.ac.uk/projects/qm-dsp
    """
    def __init__(self, sr, neighbourhoodLimit=1, segmentTypes=4):
        """
        Args:
            sr (int): required sample rate to work at
            neighbourhoodLimit (Optional[float]): minimum length of segment (in seconds). Defaults to 1s
            segmentTypes (Optional[int]): desired number of target segment types. Defaults to 4.

        """
        super(ConstQSegmentExtractor, sr).__init__()
        self.neighbourhoodLimit = neighbourhoodLimit
        self.segmentTypes = segmentTypes
        # create new QM segmenter instance
        self.qmsegmenter = qmsegmenter.ClusterMeltSegmenter(self.makeParams())
        self.qmsegmenter.initialise(sr)                 # initialise instance


    def processFrame(self, frame):
        """Process a single frame of input signal using feature extraction algorithm
        Args:
            frame (complex array): data for one audio frame for processing, in frequency domain
        """
        self.qmsegmenter.extractFeatures(frame)         # pass frame to QM segmenter for processing

    def processRemaining(self):
        """Calculate any remaining audio features after processing each frame.

        Calling function will cause analysis to use information gathered from frames so far analysed. processRemaining()
        should usually be called after processing all audio frames using processFrames().
        """
        self.qmsegmenter.segment(self.segmentTypes)     # perform segmentation using QM DSP segmenter
        # now fetch all of our features
        self._features = self.qmsegmenter.getSegmentation()
        self._done = True                               # state flag to allow us to

    @property
    def frameDomain(self):
        return BlockDomain.frequency                    # plugin requires frequency domain signals

    @property
    def blockSize(self):
        return self.qmsegmenter.getWindowsize()         # get desired window (block) size from QM segmenter instance

    @property
    def stepSize(self):
        return self.qmsegmenter.getHopsize()            # get desired hop size from QM segmenter instance

    def makeParams(self):
        params = qmsegmenter.ClusterMeltSegmenterParams()
        params.featureType = qmsegmenter.FEATURE_TYPE_CONSTQ        # set feature type to Hybrid (Const Q) --- our chosen approach
        params.nComponents = 20                         # internal QM DSP parameter for frequency bins
        # configure neighbourhood limit in samples, and pad slightly
        params.neighbourhoodLimit = int(self.neighbourhoodLimit / params.hopSize + 0.0001)
        return params

class LoudnessExtractor(GenericExtractor):
    """Process and store the windowed RMS of a signal.
    Attributes:
        sr (int): Working sample rate (in samples/sec) of feature extractor
        blockSize (int): Size of RMS window
        stepSize (int): Size of RMS step
        frameDomain (BlockDomain):
        features (np.array): Array of block RMS values.

        """

    def __init__(self, sr, blockSize=1024):

        super(LoudnessExtractor, sr).__init__()
        self._blockSize = 1024
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

