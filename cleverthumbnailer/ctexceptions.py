"""Module containing all custom exception classes used in the cleverthumbnailer
application"""

class FileNotFoundError(Exception):
    """Error class representing a problem finding some file"""
    pass

class FileFormatNotSupportedError(Exception):
    """Raised when a file format is encountered that cannot be processed"""
    pass

class SoXError(Exception):
    """Error class representing a problem running the SoX audio thumbnailing
    sub-process"""
    pass

class NoFeaturesExtractedError(Exception):
    """Error representing a failure to extract any audio features from a
    waveform"""
    pass