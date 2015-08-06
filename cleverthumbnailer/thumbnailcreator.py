import os
import exceptions
import pysox
import logging

_logger = logging.getLogger(__name__)

def createThumbnail(inFile, outFile, startSeconds, durationSeconds, fade):
    """Create an audio thumbnail from an input file

    Args:
        inFile(string): Input file name
        outFile(string): Output file name
        startSeconds(float): Start time in seconds
        durationSeconds(float): duration in seconds
        fadeIn(float): fade up time in seconds
        fadeOut(float): fade out time in seconds
    """
    _logger.debug('Creating thumbnail from track {0} to track {1} with fade'
                  ' times {2}. Starting at {3}s, duration {4}s.'.format(
        inFile, outFile, fade, startSeconds, durationSeconds) )

    if not os.path.isfile(inFile):
        raise exceptions.FileNotFoundError('Input file not found when '
                                               'creating thumbnail')

    # don't worry about validation of start and end, as sox does this
    app = pysox.CSoxApp(inFile, outFile,
                        effectparams=[('trim', [startSeconds,
                                                durationSeconds]), ])
    app.flow()