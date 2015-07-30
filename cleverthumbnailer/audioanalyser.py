#!/usr/bin/env python
"""Class to undertaken audio feature analysis"""

from featureextractor import ConstQSegmentExtractor, LoudnessExtractor, ApplauseExtractor
from audiodata import AudioData
from enum import Enum

class AnalysisBehaviour(Enum):
    LOUDNESS = 0
    DYNAMIC = 1

class AudioAnalyser(object):
    def __init__(self, fade=(0.5,0.5), crop=(7,7), length=30, dynamic=False, applause=True):
        self.fadeTimes = fade
        self.cropLength = crop
        self.thumbLength = length
        self.behaviour = AnalysisBehaviour.DYNAMIC if dynamic else AnalysisBehaviour.LOUDNESS
        self.loaded = False
        self.applause = applause
        self.audio = None

    def loadAudio(self, fileName):
        self.audio = AudioData(fileName)
        self.loaded = True

    def processAll(self):
        """Process all audio according to feature extractor plugins"""
        for featureExtractor in self.features:
            featureExtractor.processRemaining()

    def processFrames(self):
        """Process all frames of audio according to feature extractor plugins

        Currently assumes a fixed block and window size."""
        # TODO: Change block/window size handling
        for frame in self.audio.frames(self.windowSize):
            for featureExtractor in self.features:
                featureExtractor.process(frame)


