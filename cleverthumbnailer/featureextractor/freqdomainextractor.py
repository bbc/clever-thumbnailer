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
        return self.processFrame(fft.fft(samples), timestamp, *args, **kwargs)
