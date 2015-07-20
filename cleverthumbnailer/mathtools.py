__author__ = 'Jon'

def interpolate(earlyXY, lateXY, interX):
    """Given two 2D points, interpolate a Y value from an intermediate X value

    Args:
        earlyXY: Left-hand tuple of 2D point in form (x, y)
        lateXY: Right-hand tuple of 2D point in form (x, y)
        interX: X value between early and late to base interpolation on

    Returns:
        interY: Interpolated calculated Y value

    Raises:
        ValueError: when interX is not between earlyX and earlyY
    """
    earlyX, earlyY = earlyXY        # unbundle tuples
    lateX, lateY = lateXY

    xRatio = (abs(interX-earlyX)*1. / abs(lateX-earlyX)*1.)  # get the ratio of early to late values to use
    yDifference = abs(lateY-earlyY)     # get the amount difference between two known Y values
    # result is the ratio of X multiplied by the difference in two Y values, plus the DC offset
    result = (xRatio * yDifference) + min(earlyY, lateY)
    return result

if __name__ == '__main__':
    tryA = (10,10)
    tryB = (20,30)
    print(interpolate(tryA, tryB))

