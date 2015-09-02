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

import numpy

from cleverthumbnailer.utils import mathtools


class GenericExtractor(object):
    """Base class for several audio feature extraction algorithms.

    Feature extractors process audio in small (typically 512-2048 big) blocks
    of time or frequency domain samples. Each block is processed iteratively
    and then the whole audio signal post-analysed once this has been completed.
    A feature extractor is configured at initialisation with (minimally) an
    audio sample rate.

    Attributes:
        sr (int): Working sample rate (in samples/sec) of feature extractor
        blockSize (int): Size of block or window to be processed
        stepSize (int): Size of expected step between iterated blocks
        frameDomain (BlockDomain): required domain of input signals (frequency
            or time)
        features (dict): features extracted so far
    """

    def __init__(self, sr):
        """
        Args:
            sr(int): Working sample rate (in samples/sec) of feature extractor
        Raises:
            TypeError: If `sr` is not a positive whole number
        """
        try:  # test for positive integer
            assert sr >= 0
            assert (sr * 1.0).is_integer()
        except (TypeError, AssertionError, AttributeError):
            raise TypeError('Sample Rate sr must be a positive integer')

        self.sr = sr
        self._features = None
        self._done = False

    def processAllAudio(self, audioSamples):
        """Process stream of audio based on list (frames)

        Args:
            audioSamples(list): 1D list of audio samples for input

        """

        assert numpy.ndim(audioSamples) == 1
        for i, frame in enumerate(
                mathtools.windowDiscard(audioSamples, self.stepSize,
                                        self.blockSize)):
            self.processTimeDomainFrame(frame, i * self.stepSize)
        self.processRemaining()

    def processTimeDomainFrame(self, *args, **kwargs):
        """Process time domain audio frame"""
        raise NotImplementedError

    def processFrame(self, frame, timestamp):
        """Process a single frame of input signal using feature extraction algorithm
        Args:
            frame (array-like): data for one audio frame for processing
        Timestamp:
            timestamp (int): time, in samples, of beginning of frame
        """
        raise NotImplementedError()

    def processRemaining(self):
        """Calculate any remaining audio features after processing each frame.

        Calling function will cause analysis to use information gathered from
        frames so far analysed. processRemaining() should usually be called
        after processing all audio frames using processFrames().
        """
        raise NotImplementedError

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
    def done(self):
        """Indicate whether feature extractor processing has finished"""
        return self._done

    @property
    def features(self):
        """Get all features extracted by plugin from audio"""
        return self._features

    def inSamples(self, secs):
        """Convert a time in seconds to number of samples"""
        return mathtools.inSamples(self.sr, secs)

    def inSeconds(self, samples):
        """Convert a time in samples to a time in seconds"""
        return mathtools.inSeconds(self.sr, secs)

    def tupleToTimestamp(self, someTuple):
        """Convert a tuple (such as a thumbnail) of samples to a tuple of
        strings representing hh:mm:ss times"""
        return mathtools.tupleToTimestamp(self.sr, someTuple)

    def sampleToTimestamp(self, sampleN):
        """Convert a time in samples to string (hh:mm:ss) representation"""
        return mathtools.samplesToTimestamp(self.sr, sampleN)

    @property
    def frameDomain(self):
        """Indicate what domain is expected for input to the feature extractor.
        Implemented in subclasses

        Raises:
            NotImplementedError: if this method is not overridden by a subclass
        """
        raise NotImplementedError