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

import sys
import os
import argparse
import logging

from cleverthumbnailer import ctexceptions, ctconstants, thumbnailcreator, \
    audioanalyser, configurator

logging.basicConfig()
_logger = logging.getLogger()


def main(args=None):
    """Get arguments, analyse audio, and create thumbnail

    Args:
        args(list), optional: Command-line arguments for application

    Returns:
        int: exit code (0 for success)

    """
    if not args:
        args = sys.argv[1:]

    # Check for config file
    cfg = configurator.getConfiguration()  # get or create configuration
    defaultsConfig = dict(cfg.items('DEFAULTS'))

    # Use argparse to parse commandline outputs and provide UI
    parsedArgs = parseArgs(args, defaultsConfig)

    # set logging level according to args
    if parsedArgs.quiet:
        _logger.setLevel(logging.ERROR)
    elif parsedArgs.verbose == 0:
        _logger.setLevel(logging.WARN)
    elif parsedArgs.verbose == 1:
        _logger.setLevel(logging.INFO)
    elif parsedArgs.verbose >= 2:
        _logger.setLevel(logging.DEBUG)

    # instantiate audioAnalyser, which will do all audio analysis
    _logger.info('Starting analyser')
    analyser = audioanalyser.AudioAnalyser(
        parsedArgs.crop,
        parsedArgs.length,
        parsedArgs.dynamic,
        not parsedArgs.noapplause
    )

    # load audio file
    _logger.info('Loading audio')
    try:
        analyser.loadAudio(parsedArgs.input)
    except (ctexceptions.FileFormatNotSupportedError, IOError):
        _logger.error('Problem loading audio file, exiting...')
        return 1

    # do all feature extraction
    _logger.info('Processing audio')
    analyser.processAll()
    _logger.info('Audio processed!')

    # get & calculate thumbnail in and out points
    thumbStart, thumbEnd = analyser.thumbnail
    thumbStartInSeconds = analyser.inSeconds(thumbStart)
    thumbEndInSeconds = analyser.inSeconds(thumbEnd)
    _logger.info('Creating thumbnail from {0}s to {1}s'.format(
        thumbStartInSeconds, thumbEndInSeconds
    ))
    # get output file name
    outputFile = parsedArgs.output.name if parsedArgs.output else \
        createOutputFileName(
            parsedArgs.input.name,
            cfg.get('IO', 'defaultoutputfileappend'))

    # build thumbnail
    try:
        thumbnailcreator.createThumbnail(
            parsedArgs.input.name,
            outputFile,
            thumbStartInSeconds,
            (thumbEndInSeconds - thumbStartInSeconds),
            parsedArgs.fade,
        )
        _logger.info('Created thumbnail {0}'.format(outputFile))
    except ctexceptions.SoXError:
        _logger.error('Creation of thumbnail for {0} failed'.format(
            parsedArgs.input.name))
        return 1

    _logger.info('Exiting...')
    return 0  # success exit code


def parseArgs(cmdargs, defaults):
    """
    Parse command line arguments for entry into application

    Args:
        args(list): list of string arguments to be parsed

    Throws:
        SystemExit: if arguments are not syntactically valid"""

    p = argparse.ArgumentParser(prog=ctconstants.APPNAME,
                                description=ctconstants.DESCRIPTION)
    p.add_argument(
        'input',
        help='WAVE / BWF file for processing',
        type=argparse.FileType('rb'),
        metavar='input')
    p.add_argument(
        '-v',
        '--verbose',
        help='Increase logging verbosity level',
        action='count')
    p.add_argument(
        '-q',
        '--quiet',
        help='Only print warnings and errors',
        action='store_true',
    )
    p.add_argument(
        '-f',
        '--fade',
        help='Fade in and out times (seconds)',
        nargs=2,
        type=float,
        metavar=('in', 'out'),
        default=(
            float(defaults['fadein']), float(defaults['fadeout'])
        ),
    )
    p.add_argument(
        '-c',
        '--crop',
        help='Crop time (seconds)',
        nargs=2,
        type=float,
        metavar=('in', 'out'),
        default=(
            float(defaults['cropstart']), float(defaults['cropend'])
        ),
    )

    p.add_argument(
        '-l',
        '--length',
        help='Thumbnail length (seconds)',
        type=float,
        metavar='seconds',
        default=float(defaults['thumbnaillength']),
    )
    p.add_argument(
        '-d', '--dynamic',
        help='Whether to use dynamic or loudest (default) metric for ' +
             'choosing segments',
        action='store_true')
    p.add_argument(
        '-n',
        '--noapplause',
        help='Skip applause detection',
        action='store_true')
    p.add_argument(
        '-o',
        '--output',
        help='Output file path',
        type=argparse.FileType('wb'),
        metavar='wavfile')

    # parse args and throw SystemExit if invalid
    return p.parse_args(cmdargs)


def createOutputFileName(originalFileName, appendString):
    """Append a string to an existing filename, preserving file extension

    Args:
        originalFileName(string): Original file name
        appendString(string): String to append to original file name

    Returns:
        string: [originalwithoutextension][appendString].[extension]"""
    noExt, ext = os.path.splitext(originalFileName)
    return ''.join([noExt, appendString, ext])


if __name__ == '__main__':
    main(sys.argv[1:])
