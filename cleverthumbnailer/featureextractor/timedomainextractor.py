from febase import GenericExtractor
from enums import BlockDomain

class TimeDomainExtractor(GenericExtractor):

    @property
    def frameDomain(self):
        return BlockDomain.time

    def processTimeDomainFrame(self, samples, timestamp, *args, **kwargs):
        return self.processFrame(samples, timestamp, *args, **kwargs)