# Copyright (C) 2015 British Broadcasting Corporation
#
# Cleverthumbnailer is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# Cleverthumbnailer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cleverthumbnailer; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import numpy

def interpolate(XY1, XY2, interX):
    """Given two 2D points, interpolate or extrapolate a Y value from an intermediate X value

    Args:
        XY1: Left-hand tuple of 2D point in form (x, y)
        XY2: Right-hand tuple of 2D point in form (x, y)
        interX: X value between early and late to base interpolation on

    Returns:
        interY: Interpolated or extrapolated calculated Y value

    Raises:
        ValueError: when interX is not between X1 and Y1, or when XY1 and XY2 are inconsistent
    """

    if(XY1[0]>XY2[0]):      # make XY1 always the lowest X value
        XY1, XY2 = (XY2, XY1)
    X1, Y1 = XY1        # unbundle tuples
    X2, Y2 = XY2
    #Edge cases
    if X1 == X2:
        if Y1 != Y2:
            raise ValueError('XY values are inconsistent')
        if interX != X1:
            raise ValueError('Extrapolation not possible for X1==X2')
        return X1, Y1   # if we're interpolating between two identical values, return this value
    xDiff = abs(X2-X1)
    yDiff = Y2-Y1
    ratio = (interX-X1+.0)/(xDiff*1.0)
    interY = (ratio * yDiff * 1.0) + Y1
    return interX, interY

def interpStats(sampledXYArray, startX, endX):
    """Return the mean of a linearly interpolated XY array between a start and end point.

    Given an array of of XY coordinates, this function calculates the mean value between two values of X.

    Args:
        sampledXYArray (array-like): set of 2D tuples providing the XY samples, assume sorted by X value.
        startSample: the X value to start averaging from
        endSample: the X value to end averaging at

    Returns:
        mean (float): The integrated mean value

    """

    startArrayInsertionPosition, startInterpolationPoint = searchAndInterpolate(sampledXYArray, startX)
    endArrayInsertionPosition, endInterpolationPoint = searchAndInterpolate(sampledXYArray, endX, side='right')
    # slice the part of the original array we need out of it, and surround with interpolated points
    signalWithInterpolatedPoints = numpy.concatenate(([startInterpolationPoint],
                              sampledXYArray[startArrayInsertionPosition:endArrayInsertionPosition],
                              [endInterpolationPoint]))
    # transpose array so we can manipulate it
    signalX, signalY = numpy.transpose(signalWithInterpolatedPoints)
    xDiff = signalX[-1] - signalX[0]

    # return the mean (definite integral / difference in X)
    meanVal = numpy.trapz(signalY, signalX)/xDiff
    minY = numpy.min(signalY)
    maxY = numpy.max(signalY)

    return meanVal, minY, maxY

def interpMean(sampledXYArray, startX, endX):
    meanVal, _, _ = interpStats(sampledXYArray, startX, endX)
    return meanVal

def searchAndInterpolate(sampledXYArray, sample, side='left'):
    """Find the amplitude of a particular sample, given an undersampled array of values, using interpolation"""
    arrayXVals = numpy.transpose(sampledXYArray)[0]
    if sample < min(arrayXVals):
        return 0, sampledXYArray[0]
    if sample > max(arrayXVals):
        return len(sampledXYArray), sampledXYArray[-1]
    arrayInsertionPoint = numpy.searchsorted(arrayXVals, sample,side)
    start = sampledXYArray[max(0, arrayInsertionPoint-1)]
    end = sampledXYArray[min(arrayInsertionPoint, len(sampledXYArray)-1)]
    interpVal = (interpolate(start, end, sample))
    return arrayInsertionPoint, interpVal

def windowDiscard(seq, stepSize, windowSize):
    """Iterate and window sequence based on stepSize"""
    # TODO: Make an iterator-compatible (faster) version
    lenX = len(seq)
    for i in range(0, lenX, stepSize):
        if i+windowSize > lenX:
            break
        yield seq[i:i+windowSize]

def coerceThumbnail(start, end, songLength):
    """Move thumbnail to within song range.
    Args:
        start(int): thumbnail start time in samples
        end(int): thumbnail end time in samples
        songLength(int): song length in samples
    Returns:
        tuple(start, end): new thumbnail

    Raises:
        ValueError: if length is greater than end-start
    """
    if (end-start) >= songLength:
        raise ValueError('Song length is shorter than thumbnail to be created')

    if end > songLength:
        overFlow = end - songLength
        start -= overFlow
        end -= overFlow

    if start < 0:
        end += -1*start
        start = 0

    return start, end   #TODO: check