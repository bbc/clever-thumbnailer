from numpy.fft import fft

from cleverthumbnailer.enums import BlockDomain
from febase import GenericExtractor


class FrequencyDomainExtractor(GenericExtractor):

    @property
    def frameDomain(self):
        return BlockDomain.frequency

    def processTimeDomainFrame(self, samples, timestamp, *args, **kwargs):
        # TODO: Test
        return self.processFrame(fft(samples), timestamp, *args, **kwargs)
