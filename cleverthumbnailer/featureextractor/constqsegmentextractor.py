#!/usr/bin/env python
__author__ = 'Jon'

import qmsegmenter
import febase
from enums import BlockDomain
from cleverthumbnailer.segment import Segment


class ConstQSegmentExtractor(febase.GenericExtractor):
    """Wrapper for QM DSP Constant-Q Segmenter_ algorithm.

    Analyzes audio and creates a candidate set of musical sections, described by type and timestamp. Such sections
    may resemble 'chorus', 'bridge', 'verse', and are calculated based on musical similarity metrics.

    _Segmenter: https://code.soundsoftware.ac.uk/projects/qm-dsp
    """
    def __init__(self, sr, neighbourhoodLimit=4, segmentTypes=4):
        """
        Args:
            sr (int): required sample rate to work at
            neighbourhoodLimit (Optional[float]): minimum length of segment (in seconds). Defaults to 1s
            segmentTypes (Optional[int]): desired number of target segment types. Defaults to 4.

        """
        super(ConstQSegmentExtractor, self).__init__(sr)
        self.neighbourhoodLimit = neighbourhoodLimit
        self.segmentTypes = segmentTypes
        # create new QM segmenter instance
        self.qmsegmenter = qmsegmenter.ClusterMeltSegmenter(self.makeParams())
        self.qmsegmenter.initialise(sr)                 # initialise instance
        self._segInfo = None

    @property
    def segmentSampleRate(self):
        try:
            return float(self._segInfo.samplerate)
        except AttributeError:
            return None

    @property
    def nSegTypes(self):
        try:
            return int(self._segInfo.nsegtypes)
        except AttributeError:
            return None

    @property
    def features(self):
        for feature in self._segInfo.segments:
            yield Segment(int(feature.start), int(feature.end), int(feature.type))

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
        self._segInfo = self.qmsegmenter.getSegmentation()
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