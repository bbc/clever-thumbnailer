import logging
import appdirs
import os.path
import ConfigParser

from cleverthumbnailer import ctconstants, ctexceptions


_logger = logging.getLogger(__name__)


def getConfiguration():
    """Reads a configuration file using ConfigParser"""
    configFilePath = os.path.join(appdirs.user_config_dir(
        ctconstants.APPNAME), 'defaults.conf')
    try:
        appConfiguration = readConfiguration(configFilePath)
        _logger.info('Read config file {0}'.format(configFilePath))
    except (ctexceptions.FileNotFoundError, EnvironmentError):
        _logger.warn('Config file could not be read, using defaults and '
                     'creating file in {0}'.format(configFilePath))
        appConfiguration = createDefaultConfiguration()
        writeConfiguration(appConfiguration, configFilePath)
        _logger.info('Created config file {0}'.format(configFilePath))
    return appConfiguration


def readConfiguration(configFilePath):
    """Reads configuration from file

    Args:
        configFilePath(string): file path to read from

    Raises:
        FileNotFoundError: if the config file cannot be located

    Returns:
        ConfigParser(): read config object
    """
    if not os.path.isfile(configFilePath):
        raise ctexceptions.FileNotFoundError('Config file not found')

    newConfig = ConfigParser.ConfigParser()
    newConfig.read(configFilePath)
    return newConfig


def writeConfiguration(someConfig, fileLocation):
    """Write configuration to file

    Args:
        someConfig(ConfigParser()): the config object to write
        fileLocation(string): the location the config file should be written to
    """
    if not os.path.exists(os.path.dirname(fileLocation)):
        os.makedirs(os.path.dirname(fileLocation))
    try:
        with open(fileLocation, 'w') as fo:
            someConfig.write(fo)
    except EnvironmentError:
        _logger.error('Error writing config file to {0}'.format(fileLocation))


def createDefaultConfiguration():
    cfg = ConfigParser.ConfigParser()
    cfg.add_section('DEFAULTS')
    cfg.add_section('AUDIO')
    cfg.add_section('IO')

    cfg.set('DEFAULTS', 'fadein', '0.5')
    cfg.set('DEFAULTS', 'fadeout', '0.5')
    cfg.set('DEFAULTS', 'cropstart', '7')
    cfg.set('DEFAULTS', 'cropend', '7')
    cfg.set('DEFAULTS', 'thumbnaillength', '30')

    cfg.set('AUDIO', 'rmswindowsize', '1024')

    cfg.set('IO', 'defaultoutputfileappend', '_thumb')
    return cfg
