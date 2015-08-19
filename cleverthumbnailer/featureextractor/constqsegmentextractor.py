# Copyright (C) 2015 British Broadcasting Corporation
#
# Cleverthumbnailer is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# Cleverthumbnailer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cleverthumbnailer; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import logging

import qmsegmenter

from cleverthumbnailer.featureextractor.timedomainextractor import \
    TimeDomainExtractor
from cleverthumbnailer.segment import Segment


class ConstQSegmentExtractor(TimeDomainExtractor):
    """Wrapper for QM DSP Constant-Q Segmenter_ algorithm.

    Analyzes audio and creates a candidate set of musical sections, described
    by type and timestamp. Such sections may resemble 'chorus', 'bridge',
    'verse', and are calculated based on musical similarity metrics.

    _Segmenter: https://code.soundsoftware.ac.uk/projects/qm-dsp
    """

    def __init__(self, sr, neighbourhoodLimit=4, segmentTypes=4):
        """
        Args:
            sr (int): required sample rate to work at
                neighbourhoodLimit (Optional[float]): minimum length of segment
                (in seconds). Defaults to 1s
            segmentTypes (Optional[int]): desired number of target segment
                types. Defaults to 4.
        """
        self._logger = logging.getLogger(__name__)
        super(ConstQSegmentExtractor, self).__init__(sr)
        self.neighbourhoodLimit = neighbourhoodLimit
        self.segmentTypes = segmentTypes
        # create new QM segmenter instance
        self.qmsegmenter = qmsegmenter.ClusterMeltSegmenter(self.makeParams())
        self.qmsegmenter.initialise(sr)  # initialise instance
        self._logger.debug(
            'Segmenter initialised with block size ' +
            '{0} and step size {1}, sample rate {2}.'.format(
                self.blockSize,
                self.stepSize,
                self.segmentSampleRate
            ))
        self._segInfo = None
        self._features = []

    def processFrame(self, frame, timestamp=None):
        """Process a single frame of input signal using feature extraction
        algorithm.

        Args:
            frame (complex array): data for one audio frame for processing,
            in frequency domain
        """
        self.qmsegmenter.extractFeatures(
            frame)  # pass frame to QM segmenter for processing

    def processRemaining(self):
        """Calculate any remaining audio features after processing each frame.

        Calling function will cause analysis to use information gathered from
        frames so far analysed. processRemaining() should usually be called
        after processing all audio frames using processFrames().
        """

        # perform segmentation using QM DSP segmenter
        self.qmsegmenter.segment(self.segmentTypes)
        # now fetch all of our features
        self._segInfo = self.qmsegmenter.getSegmentation()

        for i, feature in enumerate(self._segInfo.segments):
            newSegment = Segment(
                int(feature.start), int(feature.end), int(feature.type))
            self._features.append(newSegment)
            self._logger.debug('Found segment #{0}: {1}'.format(i, newSegment))
        # state flag to allow us to
        self._done = True

    def makeParams(self):
        """Create default set of parameters for segmenter plugin.

        Returns:
            params(ClusterMeltSegmenterParams): set of default parameters

        """

        params = qmsegmenter.ClusterMeltSegmenterParams()
        # set feature type to Hybrid (Const Q) --- our chosen approach
        params.featureType = qmsegmenter.FEATURE_TYPE_CONSTQ
        # internal QM DSP parameter for frequency bins
        params.nComponents = 20
        # configure neighbourhood limit in samples, and pad slightly
        params.neighbourhoodLimit = int(
            self.neighbourhoodLimit / params.hopSize + 0.0001)
        return params

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
    def blockSize(self):
        # get desired window (block) size from QM segmenter instance
        return self.qmsegmenter.getWindowsize()

    @property
    def stepSize(self):
        # get desired hop size from QM segmenter instance
        return self.qmsegmenter.getHopsize()
