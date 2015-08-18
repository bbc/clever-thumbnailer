import os
import logging
import subprocess

import ctexceptions

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
        inFile, outFile, fade, startSeconds, durationSeconds)
    )

    if not os.path.isfile(inFile):
        raise ctexceptions.FileNotFoundError('Input file not found when '
                                'creating thumbnail')

    s = ['sox', str(inFile), str(outFile), 'trim', str(startSeconds),
         str(durationSeconds), 'fade', 't', str(fade[0]), str(durationSeconds),
         str(fade[1])]
    _logger.debug('Calling sox with parameters: {0}'.format(' '.join(s)))

    try:
        subprocess.call(s)
    except subprocess.CalledProcessError:
        _logger.error('Error using SoX to create thumbnail, using '
                      'parameters: {0}'.format(s))
        raise ()
