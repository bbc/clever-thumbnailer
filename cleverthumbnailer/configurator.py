import logging
import os.path
import ConfigParser

from cleverthumbnailer.utils import appdirs
from cleverthumbnailer import ctconstants, ctexceptions

_logger = logging.getLogger(__name__)


def getConfiguration():
    """Reads a configuration file using ConfigParser"""

    configFilePath = getDefaultConfigFile()
    # try reading an existing configuration
    try:
        appConfiguration = readConfiguration(configFilePath)
        _logger.info('Read config file {0}'.format(configFilePath))
    # create a new config file if needed
    except (ctexceptions.FileNotFoundError, EnvironmentError):
        _logger.warn('Config file could not be read, using defaults and '
                     'creating file in {0}'.format(configFilePath))
        appConfiguration = createDefaultConfiguration()
        writeConfiguration(appConfiguration, configFilePath)
        _logger.info('Created config file {0}'.format(configFilePath))
    # return the read or created ConfigParser object
    return appConfiguration

def getDefaultConfigFile():
    """Get the default path for a cleverthumbnailer config file

    Uses appdir module to fetch an OS-specific config directory. Config file
    is created as defaults.conf

    Returns:
        string: config file path
    """
    return os.path.join(appdirs.user_config_dir(
        ctconstants.APPNAME), 'defaults.conf')

def readConfiguration(configFilePath):
    """Read configuration from file

    Uses Python ConfigParser to read config options from a file.

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
    """Create a full set of configuration data for cleverthumbnailer.

    Uses ConfigParser to create a set of configuration options.

    Returns:
        ConfigParser: populated ConfigParser object to be used by application
    """

    cfg = ConfigParser.ConfigParser()
    # three main sections of config
    cfg.add_section('DEFAULTS')
    cfg.add_section('AUDIO')
    cfg.add_section('IO')

    # audio/command line behaviour defaults
    cfg.set('DEFAULTS', 'fadein', '0.5')
    cfg.set('DEFAULTS', 'fadeout', '0.5')
    cfg.set('DEFAULTS', 'cropstart', '7')
    cfg.set('DEFAULTS', 'cropend', '7')
    cfg.set('DEFAULTS', 'thumbnaillength', '30')
    cfg.set('DEFAULTS', 'prelude', '10')

    cfg.set('AUDIO', 'rmswindowsize', '1024')

    # default output file name append string
    cfg.set('IO', 'defaultoutputfileappend', '_thumb')
    return cfg
