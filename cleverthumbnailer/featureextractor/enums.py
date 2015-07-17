#!/usr/bin/env python
__author__ = 'Jon'
"""Container for feature extractor enums"""

import enum

class BlockDomain(enum.Enum):
    """Enum for expected feature extractor domain."""
    time = 1
    frequency = 2