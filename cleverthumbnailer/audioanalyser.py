#!/usr/bin/env python
"""Class to undertaken audio feature analysis"""

from featureextractor import ConstQSegmentExtractor

class AudioAnalyser(object):
    def __init__(self):
        self.features = {
            'segmentation': ConstQSegmentExtractor(),
            'rmsloudness': LoudnessExtractor(),
            'applause': SpectralCentroidExtractor()
        }

    def processAll(self):
        """Process all audio according to feature extractor plugins
        """
