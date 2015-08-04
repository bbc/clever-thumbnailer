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
