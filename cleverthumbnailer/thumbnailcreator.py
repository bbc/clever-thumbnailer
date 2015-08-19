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
