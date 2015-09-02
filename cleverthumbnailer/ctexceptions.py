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