"""Module containing all custom enums used by the cleverthumbnailer
application"""

import enum

class BlockDomain(enum.Enum):
    """Enum for expected feature extractor domain."""
    time = 1
    frequency = 2


class AnalysisBehaviour(enum.Enum):
    """Possible thumbnailer behaviours."""
    LOUDNESS = 0
    DYNAMIC = 1