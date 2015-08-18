from unittest import TestCase
from mock import MagicMock, patch
from cleverthumbnailer import ctexceptions, configurator
import os


class TestConfigurator(TestCase):
    def test_createDefaultConfiguration(self):
        x = configurator.createDefaultConfiguration()
        self.assertIsNotNone(x.items('DEFAULT'))
        self.assertIsNotNone(x.items('AUDIO'))
        self.assertIsNotNone(x.items('IO'))

    def test_readConfiguration(self):
        x = configurator.readConfiguration('../../cleverthumbnailer.conf')
        self.assertIsNotNone(x.items('DEFAULT'))
        self.assertIsNotNone(x.items('AUDIO'))
        self.assertIsNotNone(x.items('IO'))

    @patch('os.path.isfile')
    def test_invalidReadConfiguraton(self):
        with self.assertRaises(ctexceptions.FileNotFoundError):
            x = configurator.readConfiguration('somepath')

    @patch('appdirs.user_config_dir')
    def test_getConfigurationExisting(self, mock_userDir):
        mock_userDir.return_value = '../../cleverthumbnailer.conf'
        x = configurator.getConfiguration()
        self.assertIsNotNone(x.items('DEFAULT'))
        self.assertIsNotNone(x.items('AUDIO'))
        self.assertIsNotNone(x.items('IO'))

    @patch('appdirs.user_config_dir')
    def test_getConfigurationNew(self, mock_userDir):
        newConfigPath = os.path.join(os.getcwd(), 'tempConfig.conf')
        mock_userDir.return_value = newConfigPath
        x = configurator.getConfiguration()
        self.assertIsNotNone(x.items('DEFAULT'))
        self.assertIsNotNone(x.items('AUDIO'))
        self.assertIsNotNone(x.items('IO'))
        self.assertEquals(os.path.isfile(newConfigPath), True)