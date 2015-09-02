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

from cleverthumbnailer.featureextractor import febase
from cleverthumbnailer import enums


class TimeDomainExtractor(febase.GenericExtractor):
    """Base class for any feature extractors that process audio in the
    time domain"""

    @property
    def frameDomain(self):
        return enums.BlockDomain.time

    def processTimeDomainFrame(self, samples, timestamp, *args, **kwargs):
        """Process time domain input frame.

        Provided for full implementation of base class.

        Args:
            samples(list): block of samples for processing
            timestamp: start timestamp of block in samples
            *args: other arguments
            **kwargs: other keyword arguments

        Returns:
            object: any output from the feature extractor's processFrame method
        """

        return self.processFrame(samples, timestamp, *args, **kwargs)

