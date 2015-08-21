from math import floor
import logging

from cleverthumbnailer import enums, audiodata, ctexceptions
from cleverthumbnailer.utils import mathtools
from cleverthumbnailer.featureextractor import constqsegmentextractor, \
    loudnessextractor, applauseextractor

_logger = logging.getLogger(__name__)


class AudioAnalyser(object):
    """Audio feature analyser and thumbnail generator"""

    # List of feature extractor classes to use
    _FEATUREEXTRACTORS = (loudnessextractor.LoudnessExtractor,
                          applauseextractor.ApplauseExtractor,
                          constqsegmentextractor.ConstQSegmentExtractor)

    def __init__(self, crop=(7, 7), length=30, prelude=10, dynamic=False,
                 applause=False):
        """
        Args:
            crop(tuple(in, out)): Seconds to ignore at beginning and end of
            audio
            length(float): Length of thumbnail to be produced
            prelude(float): Length of prelude (amount of time prior to segment
            start to thumbnail) in seconds
            dynamic(bool): Use 'largest dynamic variation' rather than
            'loudest segment' when evaluating segments to thumbnail
            applause(bool): Use applause detection
        """

        self.crop = crop
        self.thumbLengthInSeconds = length
        self.prelude = prelude
        self.behaviour = enums.AnalysisBehaviour.DYNAMIC if dynamic else \
            enums.AnalysisBehaviour.LOUDNESS
        self.loaded = False
        self.processed = False
        self.thumbnailed = False
        self.applause = applause
        self.audio = None
        self.features = None
        self._thumbnail = None
        # 'Dumb' thumbnail that takes middle section of piece
        self._dumbNail = None
        self._featureExtractors = None

    def loadAudio(self, fileName):
        """Load audio file into AudioAnalyser and instantiate feature
        extractors.

        Args:
            fileName (str): File to be loaded into audio analyser

        """

        _logger.debug('Loading file {0}'.format(fileName))

        # Load and crop audio file
        try:
            self.audio = audiodata.AudioData(fileName)
            _logger.info(
                'Length of audio file before cropping is {0}'.format(
                    self.audio.sampleToTimestamp(len(self.audio.waveData))
                ))

            # crop by passing fade in and fade out as arguments
            self.audio.crop(self.audio.inSamples(self.crop[0]),
                            self.audio.inSamples(
                                self.crop[1]))
            _logger.info('Length of audio file after cropping is {0}'.format(
                self.audio.sampleToTimestamp(len(self.audio.waveData))
            ))
            self.loaded = True
        # AudioData.__init__throws IOError or FileFormatNotSupportedError if it
        # cannot load an audio file. Catch and gracefully exit.
        except (IOError, ctexceptions.FileFormatNotSupportedError) as e:
            if e.message:
                _logger.error(e.message)
            else:
                _logger.error('File {0} could not be loaded'.format(fileName))
            raise

    @property
    def thumbLengthInSamples(self):
        return self.audio.inSamples(self.thumbLengthInSeconds)

    @property
    def thumbnail(self):
        return self._thumbnail

    def processAll(self):
        """Process all audio according to feature extractor plugins

        Populates self.thumbnail, by extracting features, running audio
        processing across all features, and then calling _pickThumbnail to
        pick an appropriate audio thumbnail"""
        if not self.loaded:
            raise AttributeError('No audio to process yet')

        # initialise feature extractors from list (constant) to facilitate
        # tests and make more modular
        try:
            self._extractFeatures()
            self.processed = True
            self._thumbnail = self._pickThumbnail()
        except ctexceptions.NoFeaturesExtractedError as e:
            _logger.warn(e.message)
            _logger.info('Creating default thumbnail')
            self._thumbnail = self.middleThumbNail

    def _extractFeatures(self):
        # instantiate all of the other feature extractors
        self._featureExtractors = {fe: fe(self.audio.sr) for fe in
                                   self._FEATUREEXTRACTORS}

        # remove the applause extractor if we don't need it
        if not self.applause:
            del self._featureExtractors[applauseextractor.ApplauseExtractor]

        # perform analysis using each feature extractor
        for key, fe in self._featureExtractors.iteritems():
            _logger.info('Analysing using {0}'.format(key.__name__))
            fe.processAllAudio(self.audio.waveData)
            if not fe.features:
                raise ctexceptions.NoFeaturesExtractedError(
                    'No features found in {0}'.format(key.__name__))

    def _pickThumbnail(self):
        """Choose an audio thumbnail according to current configuration and
        feature extraction.

        Assumes feature extraction has already been undertaken. Falls back to
        returning either:
            a) The middle x seconds of a file, in the case that not enough
            information to make a decision is available from the feature
            extractors

            b) The entire clip (0, len(clip)), in the case that the requested
            thumbnail duration is longer than the clip.

        Returns:
            tuple(start, end): Thumbnail in samples, referenced to original
            audio file.
        """
        assert self.loaded
        assert self.processed

        for fe in self._featureExtractors.itervalues():
            assert hasattr(fe, 'features')

        # assign a name to each of the feature extractors
        loudnessFE = self._featureExtractors[
            loudnessextractor.LoudnessExtractor]
        segmentFE = self._featureExtractors[
            constqsegmentextractor.ConstQSegmentExtractor]

        # check the feature extractors have the methods we need
        assert hasattr(loudnessFE, 'getStats')

        # copy out the segments from the segment extractor
        segments = [segment for segment in segmentFE.features]

        # if we can't find any segments, fall back onto
        if len(segments) < 1:
            _logger.warn(
                'No musical segments identified for use; '
                'reverting to extracting middle of audio. ')
            return self.middleThumbNail  # return the old-fashioned thumbnail

        for segment in segments:
            # get RMS loudness statistics for section
            meanLoudness, minLoudness, maxLoudness = \
                loudnessFE.getStats(segment.start, segment.end)
            # store the correct metric for loudness of a segment: either
            # greatest dynamic range, or mean RMS
            segment.loudness = (maxLoudness - minLoudness) \
                if self.behaviour is enums.AnalysisBehaviour.DYNAMIC \
                else meanLoudness

            # if we're analysing applause too, check each segment for
            # presence of applause
            if applauseextractor.ApplauseExtractor in self._featureExtractors:
                applauseFE = self._featureExtractors[
                    applauseextractor.ApplauseExtractor]
                assert hasattr(applauseFE, 'checkApplause')
                segment.applause = applauseFE.checkApplause(
                    segment.start, segment.end)

        # take out sections with applause
        if applauseextractor.ApplauseExtractor in self._featureExtractors:
            validSections = [segment for segment in segments if
                             not segment.applause]
        else:
            validSections = segments

        # if there's applause in everything, revert back to all segments
        if len(validSections) < 1:
            validSections = segments
            _logger.warn(
                'Applause detected in every section. Ignoring applause'
                ' detection and continuing.')

        # sort based on loudness
        loudSections = sorted(
            validSections, key=lambda seg: seg.loudness, reverse=True)
        # should always be the case, as we've already caught when no valid
        # sections
        assert len(loudSections) > 1

        # return a thumbnail of start to start+thumblength, coerced to be
        # within the song length
        try:
            # create the thumbnail by:
            # 1. choosing start = bestSegment - prelude,
            #   end = bestSegment + thumbLength - prelude
            # 2. coercing it to fit within the bounds of the audio
            # 3. applying an offset to it so that start and end are relative
            # to original audio rather than self.waveData
            thumbnailStart = loudSections[0].start - self.prelude
            _logger.info('Chosen segment runs from {0} to {1}'.format(
                self.audio.sampleToTimestamp(loudSections[0].start),
                self.audio.sampleToTimestamp(loudSections[0].end)
            ))
            return self.offsetThumbnail(mathtools.coerceThumbnail(
                thumbnailStart,
                thumbnailStart + self.thumbLengthInSamples,
                len(self.audio.waveData)))
        except ValueError:
            _logger.warn('Requested thumbnail is longer than song; making'
                         'thumbnail of entire original (cropped) track')
            # return thumbnail pointing to cropped track
            return self.offsetThumbnail((0, len(self.audio.waveData)))

    @property
    def middleThumbNail(self):
        """Get and cache 'dumb' thumbnail start and end.

        Returns:
            tuple(start, end): thumbnail in samples, referenced to original
            audio file
        """
        if self._dumbNail:
            return self._dumbNail
        self._dumbNail = self._calculateMiddleThumbnail()
        return self._dumbNail

    def _calculateMiddleThumbnail(self):
        """Calculate 'middle X seconds' thumbnail of (cropped) audio

        Creates a thumbnail centred around the middle of self.waveData, of
         length self.length. As such, generated thumbnails respect

        Return:
            tuple(start in samples, end in samples): The thumbnail start and
            end sample positions relative to
        """
        songLength = len(self.audio.waveData)
        halfOfThumbLength = int(
            floor(self.audio.inSamples(self.thumbLengthInSeconds) / 2))
        thumbLength = halfOfThumbLength * 2

        # return original if we can't make a thumbnail
        if thumbLength >= songLength:
            _logger.warn(
                'Audio is shorter than desired thumbnail length; '
                'returning original audio.')
            return 0, songLength

        midPoint = int(songLength / 2)
        # provisional start and end points for thumbnails - may be negative or
        # overrun song length
        startPoint = midPoint - halfOfThumbLength
        endPoint = midPoint + halfOfThumbLength

        # coerce thumbnail to be within song (shift forwards/backwards if it
        # under or overruns)
        return self.offsetThumbnail(mathtools.coerceThumbnail(
            startPoint, endPoint, songLength))

    def offsetThumbnail(self, thumbnail):
        """Apply crop time offset to an audio thumbnail tuple.

        Thumbnails produced relative to self.waveData contain an in point in
        samples and an out point in samples (e.g. (1200, 1600)). These
        samples are the points in time in the *cropped* audio for which the
        thumbnail applies. This function compensates for the crop time
        applied to self.waveData, and shifts the thumbnail in and out points
        back by [self.offset] amount. The result is a thumbnail tuple whose in
        and out points (in samples) are relative to the original audio file,
        rather than the cropped version of it used internally within this
        class.

        Args:
            thumbnail (tuple): thumbnail in and out points in samples relative
            to self.waveData

        Returns:
            tuple: new thumbnail tuple with in and out points in samples
            relative to the original audio file.

        """
        newThumb = [x + self.audio.offset for x in thumbnail]
        _logger.debug('Offsetting thumbnail from {0} to {1}'.format(
            self.audio.tupleToTimestamp(thumbnail),
            self.audio.tupleToTimestamp(newThumb)
        ))
        return tuple(newThumb)
