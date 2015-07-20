#!/usr/bin/env python
__author__ = 'Jon'

def interpolate(XY1, XY2, interX):
    """Given two 2D points, interpolate a Y value from an intermediate X value

    Args:
        XY1: Left-hand tuple of 2D point in form (x, y)
        XY2: Right-hand tuple of 2D point in form (x, y)
        interX: X value between early and late to base interpolation on

    Returns:
        interY: Interpolated calculated Y value

    Raises:
        ValueError: when interX is not between X1 and Y1
    """

    if(XY1[0]>XY2[0]):      # make XY1 always the lowest X value
        XY1, XY2 = (XY2, XY1)
    X1, Y1 = XY1        # unbundle tuples
    X2, Y2 = XY2
    xDiff = abs(X2-X1)
    yDiff = Y2-Y1
    ratio = (interX-X1+.0)/(xDiff*1.0)
    return (ratio * yDiff * 1.0) + Y1


