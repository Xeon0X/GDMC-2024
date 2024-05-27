from math import sqrt, cos, pi, sin
import numpy as np


def circle(xyC, r):
    """
    Can be used for circle or disc.

    Args:
        xyC (tuple): Coordinates of the center.
        r (int): Radius of the circle.

    Returns:
        dict: Keys are distance from the circle. Value is a list of all
        coordinates at this distance. 0 for a circle. Negative values
        for a disc, positive values for a hole.
    """
    area = (
        (round(xyC[0]) - round(r), round(xyC[1]) - round(r)),
        (round(xyC[0]) + round(r) + 1, round(xyC[1]) + round(r) + 1),
    )

    circle = {}
    for x in range(area[0][0], area[1][0]):
        for y in range(area[0][1], area[1][1]):
            d = round(distance2D((x, y), (xyC))) - r
            if circle.get(d) == None:
                circle[d] = []
            circle[d].append((x, y))
    return circle


def InTriangle(point, xy0, xy1, xy2):
    # https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle#:~:text=A%20simple%20way%20is%20to,point%20is%20inside%20the%20triangle.
    dX = point[0] - xy0[0]
    dY = point[1] - xy0[1]
    dX20 = xy2[0] - xy0[0]
    dY20 = xy2[1] - xy0[1]
    dX10 = xy1[0] - xy0[0]
    dY10 = xy1[1] - xy0[1]

    s_p = (dY20 * dX) - (dX20 * dY)
    t_p = (dX10 * dY) - (dY10 * dX)
    D = (dX10 * dY20) - (dY10 * dX20)

    if D > 0:
        return (s_p >= 0) and (t_p >= 0) and (s_p + t_p) <= D
    else:
        return (s_p <= 0) and (t_p <= 0) and (s_p + t_p) >= D


def distance2D(A, B):  # TODO : Can be better.
    return sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)


def getAngle(xy0, xy1, xy2):
    """
    Compute angle (in degrees) for xy0, xy1, xy2 corner.

    https://stackoverflow.com/questions/13226038/calculating-angle-between-two-vectors-in-python

    Args:
        xy0 (numpy.ndarray): Points in the form of [x,y].
        xy1 (numpy.ndarray): Points in the form of [x,y].
        xy2 (numpy.ndarray): Points in the form of [x,y].

    Returns:
        float: Angle negative for counterclockwise angle, angle positive
        for counterclockwise angle.
    """
    if xy2 is None:
        xy2 = xy1 + np.array([1, 0])
    v0 = np.array(xy0) - np.array(xy1)
    v1 = np.array(xy2) - np.array(xy1)

    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    return np.degrees(angle)


def circlePoints(center_point, radius, number=100):
    # https://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle
    points = [
        (cos(2 * pi / number * x) * radius, sin(2 * pi / number * x) * radius)
        for x in range(0, number + 1)
    ]

    for i in range(len(points)):
        points[i] = (
            points[i][0] + center_point[0],
            points[i][1] + center_point[1],
        )

    return points


def optimizedPath(points, start=None):
    # https://stackoverflow.com/questions/45829155/sort-points-in-order-to-have-a-continuous-curve-using-python
    if start is None:
        start = points[0]
    pass_by = points
    path = [start]
    pass_by.remove(start)
    while pass_by:
        nearest = min(pass_by, key=lambda x: distance2D(path[-1], x))
        path.append(nearest)
        pass_by.remove(nearest)
    return path


def nearest(points, start):
    return min(points, key=lambda x: distance2D(start, x))


def sortRotation(points):
    """
    Sort point in a rotation order. Works in 2d but supports 3d.

    https://stackoverflow.com/questions/58377015/counterclockwise-sorting-of-x-y-data

    Args:
        points: List of points to sort in the form of [(x, y, z), (x, y,
        z)] or [(x, y), (x, y), (x, y), (x, y)]...

    Returns:
        list: List of tuples of coordinates sorted (2d or 3d).

    >>> sortRotation([(0, 45, 100), (4, -5, 5),(-5, 36, -2)])
    [(0, 45, 100), (-5, 36, -2), (4, -5, 5)]
    """
    x, y = [], []
    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][-1])
    x, y = np.array(x), np.array(y)

    x0 = np.mean(x)
    y0 = np.mean(y)

    r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)

    angles = np.where(
        (y - y0) > 0,
        np.arccos((x - x0) / r),
        2 * np.pi - np.arccos((x - x0) / r),
    )

    mask = np.argsort(angles)

    x_sorted = list(x[mask])
    y_sorted = list(y[mask])

    # Rearrange tuples to get the right coordinates.
    sortedPoints = []
    for i in range(len(points)):
        j = 0
        while (x_sorted[i] != points[j][0]) and (y_sorted[i] != points[j][-1]):
            j += 1
        else:
            if len(points[0]) == 3:
                sortedPoints.append((x_sorted[i], points[j][1], y_sorted[i]))
            else:
                sortedPoints.append((x_sorted[i], y_sorted[i]))

    return sortedPoints


def lineIntersection(line0, line1, fullLine=True):
    """
    Find (or not) intersection between two lines. Works in 2d but
    supports 3d.

    https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines

    Args:
        line0 (tuple): Tuple of tuple of coordinates.
        line1 (tuple): Tuple of tuple of coordinates.
        fullLine (bool, optional): True to find intersections along
        full line - not just in the segment.

    Returns:
        tuple: Coordinates (2d).

    >>> lineIntersection(((0, 0), (0, 5)), ((2.5, 2.5), (-2.5, 2.5)))
    """
    xdiff = (line0[0][0] - line0[1][0], line1[0][0] - line1[1][0])
    ydiff = (line0[0][-1] - line0[1][-1], line1[0][-1] - line1[1][-1])

    def det(a, b):
        return a[0] * b[-1] - a[-1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line0), det(*line1))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if not fullLine:
        if (
            min(line0[0][0], line0[1][0]) <= x <= max(line0[0][0], line0[1][0])
            and min(line1[0][0], line1[1][0])
            <= x
            <= max(line1[0][0], line1[1][0])
            and min(line0[0][-1], line0[1][-1])
            <= y
            <= max(line0[0][-1], line0[1][-1])
            and min(line1[0][-1], line1[1][-1])
            <= y
            <= max(line1[0][-1], line1[1][-1])
        ):
            return x, y
        else:
            return None
    else:
        return x, y


def circleLineSegmentIntersection(
    circleCenter, circleRadius, xy0, xy1, fullLine=True, tangentTol=1e-9
):
    """
    Find the points at which a circle intersects a line-segment. This
    can happen at 0, 1, or 2 points. Works in 2d but supports 3d.

    https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
    Note: We follow: http://mathworld.wolfram.com/Circle-LineIntersection.html

    Args:
        circleCenter (tuple): The (x, y) location of the circle center.
        circleRadius (int): The radius of the circle.
        xy0 (tuple): The (x, y) location of the first point of the
        segment.
        xy1 ([tuple]): The (x, y) location of the second point of the
        segment.
        fullLine (bool, optional): True to find intersections along
        full line - not just in the segment.  False will just return
        intersections within the segment. Defaults to True.
        tangentTol (float, optional): Numerical tolerance at which we
        decide the intersections are close enough to consider it a
        tangent. Defaults to 1e-9.

    Returns:
        list: A list of length 0, 1, or 2, where each element is a point
        at which the circle intercepts a line segment (2d).
    """

    (p1x, p1y), (p2x, p2y), (cx, cy) = (
        (xy0[0], xy0[-1]),
        (xy1[0], xy1[-1]),
        (circleCenter[0], circleCenter[1]),
    )
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** 0.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circleRadius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (
                cx
                + (
                    big_d * dy
                    + sign * (-1 if dy < 0 else 1) * dx * discriminant ** 0.5
                )
                / dr ** 2,
                cy
                + (-big_d * dx + sign * abs(dy) * discriminant ** 0.5)
                / dr ** 2,
            )
            for sign in ((1, -1) if dy < 0 else (-1, 1))
        ]  # This makes sure the order along the segment is correct
        if (
            not fullLine
        ):  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [
                (xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy
                for xi, yi in intersections
            ]
            intersections = [
                pt
                for pt, frac in zip(intersections, fraction_along_segment)
                if 0 <= frac <= 1
            ]
        if (
            len(intersections) == 2 and abs(discriminant) <= tangentTol
        ):  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections


def perpendicular(distance, xy1, xy2):
    """
    Return a tuple of the perpendicular coordinates.

    Args:
        distance (int): Distance from the line[xy1;xy2].
        xy1 (tuple): First coordinates.
        xy2 (tuple): Second coordinates.

    Returns:
        tuple: Coordinates of the line length distance, perpendicular
        to [xy1; xy2] at xy1.
    """
    (x1, y1) = xy1
    (x2, y2) = xy2
    dx = x1 - x2
    dy = y1 - y2
    dist = sqrt(dx * dx + dy * dy)
    dx /= dist
    dy /= dist
    x3 = x1 + (distance / 2) * dy
    y3 = y1 - (distance / 2) * dx
    x4 = x1 - (distance / 2) * dy
    y4 = y1 + (distance / 2) * dx
    return ((round(x3), round(y3)), (round(x4), round(y4)))


def curveCornerIntersectionPoints(
    line0, line1, startDistance, angleAdaptation=False
):
    """
    Create points between the two lines to smooth the intersection.

    Args:
        line0 (tuple): Tuple of tuple. Line coordinates. Order matters.
        line1 (tuple): Tuple of tuple. Line coordinates. Order matters.
        startDistance (int): distance from the intersection where the
        curve should starts.
        angleAdaptation (bool, optional): True will adapt the
        startDistance depending of the angle between the two lines.
        False will force the distance to be startDistance. Defaults to
        False.

    Returns:
        [list]: List of tuple of coordinates (2d) that forms the curve.
        Starts on the line and end on the other line.

    >>> curveCornerIntersectionPoints(((0, 0), (50, 20)), ((-5, 50), (25, -5)), 10)
    """
    intersection = lineIntersection(line0, line1, fullLine=True)

    if intersection == None:
        return None

    # Define automatically the distance from the intersection, where the curve
    # starts.
    if angleAdaptation:
        angle = getAngle(
            (line0[0][0], line0[0][-1]),
            intersection,
            (line1[0][0], line1[0][-1]),
        )
        # Set here the radius of the circle for a square angle.
        startDistance = startDistance * abs(1 / (angle / 90))

    startCurvePoint = circleLineSegmentIntersection(
        intersection, startDistance, line0[0], intersection, fullLine=True
    )[0]
    endCurvePoint = circleLineSegmentIntersection(
        intersection, startDistance, line1[0], intersection, fullLine=True
    )[0]
    # Higher value for better precision
    perpendicular0 = perpendicular(10e3, startCurvePoint, intersection)[0]
    perpendicular1 = perpendicular(10e3, endCurvePoint, intersection)[1]

    center = lineIntersection(
        (perpendicular0, startCurvePoint), (perpendicular1, endCurvePoint)
    )

    # Distance with startCurvePoint and endCurvePoint from the center are the
    # same.
    radius = distance2D(startCurvePoint, center)

    circle = circlePoints(
        center, round(radius), 32
    )  # n=round((2 * pi * radius) / 32)

    # Find the correct point on the circle.
    curveCornerPointsTemp = [startCurvePoint]
    for point in circle:
        if InTriangle(point, intersection, startCurvePoint, endCurvePoint):
            curveCornerPointsTemp.append(point)
    curveCornerPointsTemp.append(endCurvePoint)

    # Be sure that all the points are in correct order.
    curveCornerPoints = optimizedPath(curveCornerPointsTemp, startCurvePoint)
    return curveCornerPoints


def curveCornerIntersectionLine(
    line0, line1, startDistance, angleAdaptation=False, center=()
):
    """
    Create a continuous circular line between the two lines to smooth
    the intersection.

    Args:
        line0 (tuple): Tuple of tuple. Line coordinates. Order matters.
        line1 (tuple): Tuple of tuple. Line coordinates. Order matters.
        startDistance (int): distance from the intersection where the
        curve should starts.
        angleAdaptation (bool, optional): True will adapt the
        startDistance depending of the angle between the two lines.
        False will force the distance to be startDistance. Defaults to
        False.

    Returns:
        [list]: List of tuple of coordinates (2d) that forms the curve.
        Starts on the line and end on the other line.

    TODO:
        angleAdaptation : Set circle radius and not startDistance.
        Polar coordinates / Unit circle instead of InTriangle.

    >>> curveCornerIntersectionLine(((0, 0), (50, 20)), ((-5, 50), (25, -5)), 10)
    """
    intersection = lineIntersection(line0, line1, fullLine=True)

    if intersection == None:
        return None

    # Define automatically the distance from the intersection, where the curve
    # starts.
    if angleAdaptation:
        angle = getAngle(
            (line0[0][0], line0[0][-1]),
            intersection,
            (line1[0][0], line1[0][-1]),
        )
        # Set here the radius of the circle for a square angle.
        startDistance = startDistance * abs(1 / (angle / 90))

    startCurvePoint = circleLineSegmentIntersection(
        intersection, startDistance, line0[0], intersection, fullLine=True
    )[0]
    endCurvePoint = circleLineSegmentIntersection(
        intersection, startDistance, line1[0], intersection, fullLine=True
    )[0]
    # Higher value for better precision
    perpendicular0 = perpendicular(10e3, startCurvePoint, intersection)[0]
    perpendicular1 = perpendicular(10e3, endCurvePoint, intersection)[1]

    if center == ():
        center = lineIntersection(
            (perpendicular0, startCurvePoint), (perpendicular1, endCurvePoint)
        )

    # Distance with startCurvePoint and endCurvePoint from the center
    # are almost the same.
    radius = distance2D(startCurvePoint, center)

    circleArc = circle(center, round(radius))[0]

    # Find the correct point on the circle.
    curveCornerPointsTemp = [startCurvePoint]
    for point in circleArc:
        if InTriangle(point, intersection, startCurvePoint, endCurvePoint):
            curveCornerPointsTemp.append(point)
    # curveCornerPointsTemp.append(endCurvePoint)

    # Be sure that all the points are in correct order.
    curveCornerPoints = optimizedPath(curveCornerPointsTemp, startCurvePoint)
    return curveCornerPoints, center
