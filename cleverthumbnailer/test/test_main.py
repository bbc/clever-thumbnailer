from unittest import TestCase
from cleverthumbnailer.__main__ import main, parseArgs, getConfig
from cleverthumbnailer import exceptions
from ConfigParser import NoSectionError
from cleverthumbnailer.ctconstants import _CONFIGFILE, _DESCRIPTION, _PROG
import os
from mock import MagicMock

__author__ = 'jont'
_VALIDCONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', _CONFIGFILE))

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
            '-f 0 test.wav',
            '-f 0 0 0 test.wav',
            '-c 0 test.wav',
            '-c 0 0 0 test.wav',
            '-l nothing test.wav'
            '-n -n test.wav'
            '-f 0 0 -c 0 0 -l 0 -d -n test.wav test.wav',
        )
        for c in commands:
            with self.assertRaises(SystemExit):
                parseArgs(c.split(), self.validDefaults)