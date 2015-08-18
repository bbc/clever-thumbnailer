from cleverthumbnailer.featureextractor import febase
from cleverthumbnailer import enums

class TimeDomainExtractor(febase.GenericExtractor):

    @property
    def frameDomain(self):
        return enums.BlockDomain.time

    def processTimeDomainFrame(self, samples, timestamp, *args, **kwargs):
        return self.processFrame(samples, timestamp, *args, **kwargs)