from numpy import fft

from cleverthumbnailer.featureextractor import febase
from cleverthumbnailer import enums

class FrequencyDomainExtractor(febase.GenericExtractor):

    @property
    def frameDomain(self):
        return enums.BlockDomain.frequency

    def processTimeDomainFrame(self, samples, timestamp, *args, **kwargs):
        # TODO: Test
        return self.processFrame(fft.fft(samples), timestamp, *args, **kwargs)
