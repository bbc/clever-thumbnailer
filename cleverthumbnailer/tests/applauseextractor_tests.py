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
from unittest import TestCase

from cleverthumbnailer.featureextractor.applauseextractor import \
    ApplauseExtractor, ApplauseState
from cleverthumbnailer.audiodata import AudioData

__author__ = 'jont'
_TESTWAVE = '/home/jont/Dropbox/BBC2/Projects/Thumbnailer/Applause/' \
            '3liveinconcert_nuovamusica_1.wav'

_logger = logging.getLogger(__name__)

class TestApplauseExtractor(TestCase):
    audioData = None
    def setUp(self):
        self.audioData = AudioData(_TESTWAVE)

    def test_resizeMovAvgBuffer(self):
        self.fail()

    def test_calculateBufferMean(self):
        self.fail()

    def test_blockSize(self):
        self.fail()

    def test_stepSize(self):
        self.fail()

    def test_processFrame(self):
        self.fail()

    def test_processRemaining(self):
        self.fail()

    def test_applauseDetection(self):
        self.fail()

    # TODO: Set up mock tests to test individual modules
    def test_process(self):
        x = ApplauseExtractor(self.audioData.sr)
        x.processAllAudio(self.audioData.waveData)
        for n, feature in enumerate(x.features):
            type, timestamp = feature
            # time to minutes & seconds for readability
            m1, s1 = divmod((timestamp/x.sr),60)
            print('\tSection {0}: Type {1}. Start {2}m{3}s'.format(
                n, type, m1, s1))
        assert True