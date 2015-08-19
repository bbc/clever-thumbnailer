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

from unittest import TestCase
from mock import patch, PropertyMock

from cleverthumbnailer.audioanalyser import AudioAnalyser


class TestAudioAnalyser(TestCase):

    @patch('cleverthumbnailer.audioanalyser.AudioData')
    def test_thumbLengthInSamples(self, audioData_mock):
        audioData_mock.return_value.sr = PropertyMock(return_value=44100)
        x = AudioAnalyser()
        x.loadAudio('test.wav')
        self.assertEquals(x.inSamples(10), 441000)

    def test_thumbnail(self):
        self.fail()

    def test_processAll(self):


        self.fail()

    def test__pickThumbnail(self):
        self.fail()

    def test_middleThumbNail(self):
        self.fail()

    def test_inSeconds(self):
        self.fail()

    def test_inSamples(self):
        self.fail()
