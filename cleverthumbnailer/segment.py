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

class Segment(object):
    """Class to contain information to do with one musical segment of a song,
    as used by CleverThumbnailer"""
    def __init__(self, start, end, type):
        """
        Args:
            start (int): segment start time in (nominally in samples)
            end (int): segment end time (nominally in samples)
            type (int): enumerated segment 'type'
        """
        self.start = start
        self.end = end
        self.type = type
        self.loudness = None
        self.applause = None

    def __str__(self):
        return 'Segment start: {0}, end: {1}, type: {2}'.format(
            self.start,
            self.end,
            self.type
        )
