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

from numpy import fft

from cleverthumbnailer.featureextractor import febase
from cleverthumbnailer import enums


class FrequencyDomainExtractor(febase.GenericExtractor):
    """Base class for any feature extractors that process audio in the
    frequency domain"""

    @property
    def frameDomain(self):
        # indicate that this plugin expects input in the frequency domain
        return enums.BlockDomain.frequency

    def processTimeDomainFrame(self, samples, timestamp, *args, **kwargs):
        """Transform and process a frame input in the time domain

        Performs Fast Fouriter Transform (FFT) on block of samples for
        processing in a frequency domain-based feature extractor

        Args:
            samples(list): block of time-domain samples for processing
            timestamp: start timestamp of block in samples
            *args: other arguments
            **kwargs: other keyword arguments

        Returns:
            object: any output from the feature extractor's processFrame method
        """

        # perform FFT on time-domain frame and then pass for processing
        return self.processFrame(fft.fft(samples), timestamp, *args, **kwargs)
