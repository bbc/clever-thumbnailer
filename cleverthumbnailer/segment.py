__author__ = 'jont'

class Segment(object):
    def __init__(self, start, end, type):
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
