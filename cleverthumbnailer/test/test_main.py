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
from __main__ import main, parseArgs, getConfig
from ConfigParser import NoSectionError

from cleverthumbnailer.__main__ import main, parseArgs
from cleverthumbnailer.ctconstants import CONFIGFILE, DESCRIPTION, APPNAME

__author__ = 'jont'
_VALIDCONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONFIGFILE))

class TestMain(TestCase):
    validArgs = 'resources/test.wav'.split()
    def test_ValidConfig(self):
        main(self.validArgs, _VALIDCONFIG)


class TestGetConfig(TestCase):
    def test_getConfig(self):
        x = getConfig('')
        self.assertIsNotNone(x)
        with self.assertRaises(NoSectionError):
            x.items('DEFAULTS')
        with self.assertRaises(NoSectionError):
            x.items('AUDIO')

    def test_validConfig(self):
        x = getConfig(_VALIDCONFIG)
        self.assertIsNotNone(x)
        defaults = dict(x.items('DEFAULTS'))
        audio = dict(x.items('AUDIO'))

        for item in ('fadein', 'fadeout', 'cropstart', 'cropend', 'thumbnaillength'):
            self.assertIn(item, defaults)
        for item in [('windowsize')]:
            self.assertIn(item, audio)



class TestParseArgs(TestCase):
    validDefaults = {
        'fadein': 0,
        'fadeout': 0,
        'cropstart': 0,
        'cropend': 0,
        'thumbnaillength': 0,
        'prelude': 0
    }

    def test_validParseArgs(self):
        commands = (
            'resources/test.wav',
            '-o out.wav resources/test.wav',
            '-o out.thing resources/test.wav',
            '-f 0 0 -c 0 0 -l 0 -d -n resources/test.wav',
        )
        for c in commands:
            try:
                parseArgs(c.split(), self.validDefaults)
                assert True
            except SystemExit:
                self.assertFalse(c, 'Expression ''{0}'' caused argparse to return SystemExit'.format(c))

    def test_invalidParseArgs(self):
        commands = (
            '-o out.wav',
            '-c -5 5 in.wav',
            '-p 10 in.wav'
            # '-f 0 test.wav',
            # '-f 0 0 0 test.wav',
            # '-c 0 test.wav',
            # '-c 0 0 0 test.wav',
            # '-l nothing test.wav'
            # '-n -n test.wav'
            # '-f 0 0 -c 0 0 -l 0 -d -n test.wav test.wav',
        )
        for c in commands:
            with self.assertRaises(SystemExit):
                parseArgs(c.split(), self.validDefaults)