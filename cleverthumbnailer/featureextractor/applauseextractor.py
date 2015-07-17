#!/usr/bin/env python
__author__ = 'Jon'


class ApplauseExtractor(genericextractor.GenericExtractor):
    def __init__(self, sr, blockSize=1024):
        super(ApplauseExtractor, sr).__init__()
        self._blockSize = blockSize
        self._features = numpy.array([])