from math import sqrt
from math import pi
from math import cos, sin
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


def line(xyz1, xyz2, pixelPerfect=True):
    """
    Calculate a line between two points in 3D space.

    https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/

    Args:
        xyz1 (tuple): First coordinates.
        xyz2 (tuple): Second coordinates.
        pixelPerfect (bool, optional): Blocks will be placed diagonally,
        not side by side if pixelPerfect is True. Defaults to True.

    Returns:
        list: List of blocks.
    """
    (x1, y1, z1) = xyz1
    (x2, y2, z2) = xyz2
    x1, y1, z1, x2, y2, z2 = (
        round(x1),
        round(y1),
        round(z1),
        round(x2),
        round(y2),
        round(z2),
    )

    ListOfPoints = []
    ListOfPoints.append((x1, y1, z1))
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    if x2 > x1:
        xs = 1
    else:
        xs = -1
    if y2 > y1:
        ys = 1
    else:
        ys = -1
    if z2 > z1:
        zs = 1
    else:
        zs = -1

    # Driving axis is X-axis
    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x1 != x2:
            x1 += xs
            ListOfPoints.append((x1, y1, z1))
            if p1 >= 0:
                y1 += ys
                if not pixelPerfect:
                    if ListOfPoints[-1][1] != y1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dx
            if p2 >= 0:
                z1 += zs
                if not pixelPerfect:
                    if ListOfPoints[-1][2] != z1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz

    # Driving axis is Y-axis
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y1 != y2:
            y1 += ys
            ListOfPoints.append((x1, y1, z1))
            if p1 >= 0:
                x1 += xs
                if not pixelPerfect:
                    if ListOfPoints[-1][0] != x1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dy
            if p2 >= 0:
                z1 += zs
                if not pixelPerfect:
                    if ListOfPoints[-1][2] != z1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz

    # Driving axis is Z-axis
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z1 != z2:
            z1 += zs
            ListOfPoints.append((x1, y1, z1))
            if p1 >= 0:
                y1 += ys
                if not pixelPerfect:
                    if ListOfPoints[-1][1] != y1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dz
            if p2 >= 0:
                x1 += xs
                if not pixelPerfect:
                    if ListOfPoints[-1][0] != x1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
    return ListOfPoints


def offset(distance, xy1, xy2):
    """
    Compute the coordinates of perpendicular points from two points. 2D
    only.

    Args:
        distance (int): Distance from the line[xy1;xy2] of the
        perpendicular points.
        xy1 (tuple): First position.
        xy2 (tuple): Second position.

    Returns:
        tuple: The coordinates of perpendicular points.
        A: Perpendicular from [xy1;xy2] at distance from pos1.
        B: perpendicular from [xy1;xy2] at -distance from pos1.
        C: perpendicular from [xy2;xy1] at distance from pos2.
        D: perpendicular from [xy2;xy1] at -distance from pos2.
    """
    A, B = perpendicular(distance * 2, xy1, xy2)
    C, D = perpendicular(distance * 2, xy2, xy1)
    return ([A, D], [B, C])


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


def curve(points, number_true_pts=40, debug=False):
    """
    Returns a 3d curve.

    https://stackoverflow.com/questions/18962175/spline-interpolation-coefficients-of-a-line-curve-in-3d-space

    Args:
        points (np.array): Points where the curves should pass.
        number_true_pts (int, optional): Number of points to compute. Defaults to 40.
        debug (bool, optional): Just a visual graphic. Defaults to False.

    Returns:
        tuple: Tuple of list of each coordinate.
    """
    # Remove duplicates.
    points = tuple(map(tuple, points))
    points = sorted(set(points), key=points.index)

    x_sample = []
    y_sample = []
    z_sample = []

    for i in range(len(points)):
        x_sample.append(points[i][0])
        z_sample.append(points[i][1])
        y_sample.append(points[i][2])

    x_sample = np.array(x_sample)
    y_sample = np.array(y_sample)
    z_sample = np.array(z_sample)

    tck, u = interpolate.splprep([x_sample, y_sample, z_sample], s=2, k=2)
    x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
    u_fine = np.linspace(0, 1, number_true_pts)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    if debug:
        fig2 = plt.figure(2)
        ax3d = fig2.add_subplot(111, projection="3d")
        ax3d.plot(x_sample, y_sample, z_sample, "r*")
        ax3d.plot(x_knots, y_knots, z_knots, "go")
        ax3d.plot(x_fine, y_fine, z_fine, "r")
        fig2.show()
        plt.show()

    x = x_fine.tolist()
    z = y_fine.tolist()
    y = z_fine.tolist()

    for i in x:
        i = round(i)
    for i in y:
        i = round(i)
    for i in z:
        i = round(i)

    return x, y, z


def curveOffset(x, y, z, distance=5):
    """
    Offset a curve.

    Args:
        x (list): List of x coordinates.
        y (list): List of y coordinates.
        z (list): List of z coordinates.
        distance (int, optional): Distance of offsetting. Defaults to 5.

    Returns:
        tuple: Lists of points from the upper curve and the lower curve.

    TODO:
        The accuracy can be improved by finding the inner and outer arc:
        connect the points of the arc and not calculate their
        middle.
    """
    lineA = []
    lineB = []
    line0 = []
    line1 = []

    # Offsetting
    for i in range(len(x) - 1):
        parallel = offset(distance, (x[i], z[i]), (x[i + 1], z[i + 1]))
        lineA.append(
            (
                (parallel[0][0][0], y[i], parallel[0][0][1]),
                (parallel[0][1][0], y[i + 1], parallel[0][1][1]),
            )
        )
        lineB.append(
            (
                (parallel[1][0][0], y[i], parallel[1][0][1]),
                (parallel[1][1][0], y[i + 1], parallel[1][1][1]),
            )
        )

    # First points
    # print(x, y, z, distance)
    # print(x, len(x))
    # print("lineA:", lineA)
    # print("parallel:", parallel)
    line0.append(
        (
            round(lineA[0][0][0]),
            round(lineA[0][0][1]),
            round(lineA[0][0][2]),
        )
    )
    line1.append(
        (
            round(lineB[0][0][0]),
            round(lineB[0][0][1]),
            round(lineB[0][0][2]),
        )
    )

    # Middle of between segments
    for i in range(len(lineA) - 1):
        line0.append(
            (
                round((lineA[i][1][0] + lineA[i + 1][0][0]) / 2),
                round((lineA[i][1][1] + lineA[i + 1][0][1]) / 2),
                round((lineA[i][1][2] + lineA[i + 1][0][2]) / 2),
            )
        )
        line1.append(
            (
                round((lineB[i][1][0] + lineB[i + 1][0][0]) / 2),
                round((lineB[i][1][1] + lineB[i + 1][0][1]) / 2),
                round((lineB[i][1][2] + lineB[i + 1][0][2]) / 2),
            )
        )

    # Last points
    line0.append(
        (
            round(lineA[-1][1][0]),
            round(lineA[-1][1][1]),
            round(lineA[-1][1][2]),
        )
    )
    line1.append(
        (
            round(lineB[-1][1][0]),
            round(lineB[-1][1][1]),
            round(lineB[-1][1][2]),
        )
    )

    return line0, line1


def pixelPerfect(path):
    """
    Remove blocks that are side by side in the path. Keep the blocks
    that are in diagonal.

    Args:
        path (list): List of coordinates from a path.

    Returns:
        list: List cleaned.

    TODO:
        Add 3D.
    """
    # NotPixelPerfect detection
    if len(path) == 1 or len(path) == 0:
        return path
    else:
        notPixelPerfect = []
        c = 0
        while c < len(path):
            if c > 0 and c + 1 < len(path):
                if (
                    (
                        path[c - 1][0] == path[c][0]
                        or path[c - 1][1] == path[c][1]
                    )
                    and (
                        path[c + 1][0] == path[c][0]
                        or path[c + 1][1] == path[c][1]
                    )
                    and path[c - 1][1] != path[c + 1][1]
                    and path[c - 1][0] != path[c + 1][0]
                ):
                    notPixelPerfect.append(path[c])
            c += 1

    # Double notPixelPerfect detection
    if len(notPixelPerfect) == 1 or len(notPixelPerfect) == 0:
        return notPixelPerfect
    else:
        d = 0
        while d < len(notPixelPerfect):
            if d + 1 < len(notPixelPerfect):
                if (
                    notPixelPerfect[d][0] == notPixelPerfect[d + 1][0]
                    and (notPixelPerfect[d][1] - notPixelPerfect[d + 1][1])
                    in {1, -1}
                ) or (
                    notPixelPerfect[d][1] == notPixelPerfect[d + 1][1]
                    and (notPixelPerfect[d][0] - notPixelPerfect[d + 1][0])
                    in {1, -1}
                ):
                    notPixelPerfect.remove(notPixelPerfect[d + 1])
            d += 1

    # Remove notPixelPerfect from path
    for i in range(len(notPixelPerfect)):
        path.remove(notPixelPerfect[i])

    return path


def cleanLine(path):  # HERE
    """
    Clean and smooth a list of blocks. Works in 2d but supports 3d.

    Args:
        path (list): List of blocks.

    Returns:
        list: List cleaned.

    TODO:
        Do not work perfectly since 16/04/2021.
        Add new patterns.
        Problem with i -= 10 : solved but not understand why.
        16/04/2021.
    """

    pathTemp = []
    for i in path:
        if i not in pathTemp:
            pathTemp.append(i)
    path = pathTemp

    i = 0

    while i < len(path):

        # 2 blocks, 90 degrees, 2 blocks = 1 block, 1 block, 1 block
        if i + 3 < len(path):
            if (
                path[i][0] == path[i + 1][0]
                and path[i + 2][-1] == path[i + 3][-1]
            ):
                if len(path[i + 1]) == 3:
                    path.insert(
                        (i + 1),
                        (path[i + 2][0], path[i + 2][1], path[i + 1][-1]),
                    )
                else:
                    path.insert((i + 1), (path[i + 2][0], path[i + 1][-1]))
                del path[i + 2]  # 2nd block
                del path[i + 2]  # 3rd block
                i -= 1
                continue
            elif (
                path[i][-1] == path[i + 1][-1]
                and path[i + 2][0] == path[i + 3][0]
            ):
                if len(path[i + 1]) == 3:
                    path.insert(
                        (i + 1),
                        (path[i + 1][0], path[i + 1][1], path[i + 2][-1]),
                    )
                else:
                    path.insert(
                        (i + 1),
                        (path[i + 1][0], path[i + 2][-1]),
                    )
                del path[i + 2]  # 2nd block
                del path[i + 2]  # 3rd block
                i -= 1
                continue

        # 1 block, 3 blocks, 1 block = 1 block, 2 blocks, 2 blocks
        if i - 1 >= 0 and i + 5 <= len(path):
            if (
                (
                    path[i + 1][-1] == path[i + 2][-1]
                    and path[i + 2][-1] == path[i + 3][-1]
                )
                and (
                    path[i + 1][-1] != path[i][-1]
                    and path[i + 3][-1] != path[i + 4][-1]
                )
                and (
                    path[i - 1][-1] != path[i][-1]
                    and path[i + 4][-1] != path[i + 5][-1]
                )
            ):
                if len(path[i]) == 3:
                    path.insert(
                        (i + 1), (path[i + 1][0], path[i + 1][1], path[i][-1])
                    )
                else:
                    path.insert((i + 1), (path[i + 1][0], path[i][-1]))
                del path[i + 2]  # 2nd block
                i -= 1
                continue
            elif (
                (
                    path[i + 1][0] == path[i + 2][0]
                    and path[i + 2][0] == path[i + 3][0]
                )
                and (
                    path[i + 1][0] != path[i][0]
                    and path[i + 3][0] != path[i + 4][0]
                )
                and (
                    path[i - 1][0] != path[i][0]
                    and path[i + 4][0] != path[i + 5][0]
                )
            ):
                if len(path[i]) == 3:
                    path.insert(
                        (i + 1), (path[i][0], path[i][1], path[i + 1][-1])
                    )
                else:
                    path.insert((i + 1), (path[i][0], path[i + 1][-1]))
                del path[i + 2]  # 2nd block
                i -= 1
                continue

        i += 1

    return path


def distance2D(A, B):  # TODO : Can be better.
    return sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)


def curveSurface(
    points,
    distance,
    resolution=7,
    pixelPerfect=False,
    factor=2,
    start=0,
    returnLine=True,
):  # HERE
    """
    Create a curve with a thickness.

    Args:
        points (numpy.ndarray): Points where the curve should go.
        distance (int): Thickness.
        resolution (int, optional): Number of blocks that separate each
        point to calculate parallel curves. 0 to use the points
        calculated to create the curve. Defaults to 7.
        pixelPerfect (bool, optional): True to avoid heaps. Defaults to
        False.
        factor (int, optional): Number of sub-line that will be
        calculated to avoid hole with coordinates. Defaults to 2.

    Returns:
        dict: Key 0 is the list of coordinates of the center line.
        Positive keys are lists of coordinates of lines on the right
        side, negative keys are for the left side.

    >>> curveSurface(
            np.array(
                [
                    [12, 248, -103],
                    [-5, 219, -85],
                    [-22, 205, -128],
                    [-51, 70, -240],
                    [40, 198, -166],
                    [19, 241, -102],
                    [-6, 62, -223],
                ]
            ),
            5,
            resolution=7,
        )
    """
    if len((points)) >= 3:
        # Calculate resolution of the main curve depending of the total curve length.
        lenCurve = 0
        for i in range(len(points) - 1):
            lenCurve += sqrt(
                ((points[i][0] - points[i + 1][0]) ** 2)
                + ((points[i][1] - points[i + 1][1]) ** 2)
                + ((points[i][2] - points[i + 1][2]) ** 2)
            )
        number_true_pts = round(lenCurve / 6)

        # Calculate the main line.
        X, Y, Z = curve(points, number_true_pts)
        if len(X) < 2:
            X, Y, Z = (
                (points[0][0], points[1][0]),
                (points[0][1], points[1][1]),
                (points[0][2], points[1][2]),
            )
    else:
        X, Y, Z = (
            (points[0][0], points[1][0]),
            (points[0][1], points[1][1]),
            (points[0][2], points[1][2]),
        )

    centerLineTemp = []
    for i in range(len(X) - 1):
        xyz0 = X[i], Y[i], Z[i]
        xyz1 = (X[i + 1], Y[i + 1], Z[i + 1])
        centerLineTemp.extend(line(xyz0, xyz1))

    if not returnLine:
        returnPoints = []
        for i in range(len(X)):
            returnPoints.append((round(X[i]), round(Y[i]), round(Z[i])))

    # Clean the main line.
    # centerLine = cleanLine(centerLineTemp)
    centerLine = centerLineTemp

    # Offset.
    centerPoints = []

    if resolution != 0:
        for i in range(0, len(centerLine), resolution):
            centerPoints.append(centerLine[i])
    else:
        for i in range(len(X)):
            centerPoints.append((X[i], Y[i], Z[i]))

    X = [centerPoints[i][0] for i in range(len(centerPoints))]
    Y = [centerPoints[i][1] for i in range(len(centerPoints))]
    Z = [centerPoints[i][2] for i in range(len(centerPoints))]

    rightPoints = []
    leftPoints = []

    # print(centerLine, "XYZ centerPoint to offset")
    # print(cleanLine(centerLineTemp), "with cleanLine")
    for i in range(start * factor, distance * factor):
        rightPoint, leftPoint = curveOffset(X, Y, Z, i / factor)
        rightPoints.append(rightPoint)
        leftPoints.append(leftPoint)

    rightLine = []
    leftLine = []
    rightSide = []
    leftSide = []

    if returnLine == True:  # Creating lines on each side between each point.
        for i in range(len(rightPoints)):
            for j in range(len(rightPoints[i]) - 1):
                rightLine.extend(
                    line(
                        rightPoints[i][j],
                        rightPoints[i][j + 1],
                        pixelPerfect,
                    )
                )
            rightSide.append(rightLine)
            rightLine = []

        for i in range(len(leftPoints)):
            for j in range(len(leftPoints[i]) - 1):
                leftLine.extend(
                    line(
                        leftPoints[i][j],
                        leftPoints[i][j + 1],
                        pixelPerfect,
                    )
                )
            leftSide.append(leftLine)
            leftLine = []

    else:  # Do not create lines. Points instead.
        for i in range(len(rightPoints)):
            for j in range(len(rightPoints[i])):
                rightLine.append(rightPoints[i][j])
            rightSide.append(rightLine)
            rightLine = []

        for i in range(len(leftPoints)):
            for j in range(len(leftPoints[i])):
                leftLine.append(leftPoints[i][j])
            leftSide.append(leftLine)
            leftLine = []

    # Returns. 0 is the center line, positive values ​​are lines on the
    # right, negative values ​​are lines on the left.
    smoothCurveSurfaceDict = {}
    if returnLine:
        smoothCurveSurfaceDict[0] = centerLine
    else:
        smoothCurveSurfaceDict[0] = returnPoints

    countLine = 0
    for l in rightSide:
        # l = cleanLine(l)
        countLine += 1
        smoothCurveSurfaceDict[countLine] = l
    countLine = 0
    for l in leftSide:
        # l = cleanLine(l)
        countLine -= 1
        smoothCurveSurfaceDict[countLine] = l

    return smoothCurveSurfaceDict


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


def circleIntersections(xy0, r0, xy1, r1):
    # https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles

    x0, y0 = xy0
    x1, y1 = xy1
    d = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # Non intersecting.
    if d > r0 + r1:
        return None
    # One circle within other.
    if d < abs(r0 - r1):
        return None
    # Coincident circles.
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        return ((x3, y3), (x4, y4))


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


def circlePoints(xyC, r, n=100):
    # https://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle
    points = [
        (cos(2 * pi / n * x) * r, sin(2 * pi / n * x) * r)
        for x in range(0, n + 1)
    ]

    for i in range(len(points)):
        points[i] = (
            points[i][0] + xyC[0],
            points[i][1] + xyC[1],
        )

    return points


def optimizedPath(coords, start=None):
    # https://stackoverflow.com/questions/45829155/sort-points-in-order-to-have-a-continuous-curve-using-python
    if start is None:
        start = coords[0]
    pass_by = coords
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


def middleLine(xyz0, xyz1):
    x = (xyz0[0] + xyz1[0]) / 2
    z = (xyz0[-1] + xyz1[-1]) / 2
    if len(xyz0) <= 2:
        return (x, z)
    else:
        y = (xyz0[1] + xyz1[1]) / 2
        return (round(x), round(y), round(z))
