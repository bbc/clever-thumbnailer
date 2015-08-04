#!/usr/bin/env python
"""Class to undertaken audio feature analysis"""
from math import floor
import logging

from cleverthumbnailer.enums import AnalysisBehaviour as Behaviour
from featureextractor import ConstQSegmentExtractor, LoudnessExtractor, ApplauseExtractor
from mathtools import coerceThumbnail
from audiodata import AudioData
_logger = logging.getLogger(__name__)

class AudioAnalyser(object):
    _FEATUREEXTRACTORS = (ConstQSegmentExtractor, LoudnessExtractor, ApplauseExtractor)
    def __init__(self, fade=(0.5,0.5), crop=(7,7), length=30, dynamic=False, applause=True):
        self.fadeTimesInSeconds = fade   # in seconds
        self.cropLengthsInSeconds = crop  # in seconds
        self.thumbLengthInSeconds = length   # in seconds
        self.behaviour = Behaviour.DYNAMIC if dynamic else Behaviour.LOUDNESS
        self.loaded = False
        self.processed = False
        self.thumbnailed = False
        self.applause = applause
        self.audio = None
        self.segmentExtractor = None
        self.loudnessExtractor = None
        self.applauseExtractor = None
        self.features = None
        self._thumbnail = None
        self._dumbNail = None   # 'Dumb' thumbnail that takes middle section of piece

    def loadAudio(self, fileName):
        self.audio = AudioData(fileName)
        self.loaded = True

        # initialise feature extractors
        self.loudnessExtractor = LoudnessExtractor(self.audio.sr)   #TODO: Add other params
        self.applauseExtractor = ApplauseExtractor(self.audio.sr)
        self.segmentExtractor = ConstQSegmentExtractor(self.audio.sr)

    @property
    def fadeTimeInSamples(self):
        return tuple([self.inSamples(x) for x in self.fadeTimesInSeconds])

    @property
    def cropLengthsInSamples(self):
        return tuple([self.inSamples(x) for x in self.cropLengthsInSeconds])

    @property
    def thumbLengthInSamples(self):
        return self.inSamples(self.thumbLengthInSeconds)

    @property
    def thumbnail(self):
        return self._thumbnail  #TODO: Work out what to do here if called before processing

    def processAll(self):
        """Process all audio according to feature extractor plugins"""
        if not self.loaded:
            raise
        self.loudnessExtractor.processAllAudio(self.audio.waveData) #TODO: Tidy into iterator
        self.applauseExtractor.processAllAudio(self.audio.waveData)
        self.segmentExtractor.processAllAudio(self.audio.waveData)
        assert self.loudnessExtractor.features
        assert self.applauseExtractor.features
        assert self.segmentExtractor.features
        self.processed = True
        self._thumbnail = self._pickThumbnail()


    def _pickThumbnail(self):
        assert self.loaded
        assert self.processed
        segments = [segment for segment in self.segmentExtractor.features]  # copy out our segments

        if len(segments) < 1:
            _logger.warn('No musical segments identified for use; reverting to extracting middle of audio. ')
            return self.middleThumbNail    # return the old-fashioned thumbnail

        for segment in segments:
            # get RMS loudness statistics for section
            meanLoudness, minLoudness, maxLoudness = self.loudnessExtractor.getStats(segment.start, segment.end)
            # store the correct metric for loudness of a segment: either greatest dynamic range, or mean RMS
            segment.loudness = (maxLoudness - minLoudness) if self.behaviour is Behaviour.DYNAMIC else meanLoudness
            # if we're analysing applause too, check each segment for presence of applause
            if self.applause:
                segment.applause = self.applauseExtractor.checkApplause(segment.start, segment.end)

        # take out sections with applause
        validSections = [segment for segment in segments if not segment.applause]

        # if there's applause in everything, revert back to all segments
        if len(validSections) < 1:
            validSections = segments
            _logger.warn('Applause detected in every section. Ignoring applause detection and continuing.')

        # sort based on loudness
        loudSections = sorted(validSections, key=lambda segment: segment.loudness, reverse=True)
        assert len(loudSections) > 1    # should always be the case, as we've already caught when no valid sections

        # return a thumbnail of start to start+thumblength, coerced to be within the song length
        return coerceThumbnail(
            loudSections[0].start,
            loudSections[0].start+self.thumbLengthInSamples,
            len(self.audio.waveData))


    @property
    def middleThumbNail(self):
        """Get and cache 'dumb' thumbnail start and end."""
        if self._dumbNail:
            return self._dumbNail

        songLength = len(self.audio.waveData)
        halfOfThumbLength = int(floor(self.inSamples(self.thumbLengthInSeconds)/2))
        thumbLength = halfOfThumbLength*2

        # return original if we can't make a thumbnail
        if thumbLength >= songLength:
            _logger.warn('Audio is shorter than desired thumbnail length; returning original audio.')
            return 0, songLength

        midPoint = int(songLength/2)
        # provisional start and end points for thumbnails - may be negative or overrun song length
        startPoint = midPoint - halfOfThumbLength
        endPoint = midPoint + halfOfThumbLength

        # coerce thumbnail to be within song (shift forwards/backwards if it under or overruns)
        self._dumbNail = coerceThumbnail(startPoint, endPoint, songLength)
        return self._dumbNail

    def inSeconds(self, sampleN):
        return 1.0*sampleN/self.audio.sr

    def inSamples(self, seconds):
        return int(seconds*self.audio.sr)