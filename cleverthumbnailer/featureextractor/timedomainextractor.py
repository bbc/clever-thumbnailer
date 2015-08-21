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

