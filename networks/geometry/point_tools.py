from math import sqrt, cos, pi, sin
import numpy as np
from networks.geometry.segment_tools import discrete_segment, middle_point


def circle(center, radius):
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
        (round(center[0]) - round(radius), round(center[1]) - round(radius)),
        (round(center[0]) + round(radius) + 1,
         round(center[1]) + round(radius) + 1),
    )

    circle = {}
    for x in range(area[0][0], area[1][0]):
        for y in range(area[0][1], area[1][1]):
            d = round(distance((x, y), (center))) - radius
            if circle.get(d) == None:
                circle[d] = []
            circle[d].append((x, y))
    return circle


def is_in_triangle(point, xy0, xy1, xy2):
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


def distance(xy1, xy2):  # TODO : Can be better.
    return sqrt((xy2[0] - xy1[0]) ** 2 + (xy2[-1] - xy1[-1]) ** 2)


def get_angle(xy0, xy1, xy2):
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


def circle_points(center_point, radius, number=100):
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


def optimized_path(points, start=None):
    # https://stackoverflow.com/questions/45829155/sort-points-in-order-to-have-a-continuous-curve-using-python
    if start is None:
        start = points[0]
    pass_by = points
    path = [start]
    pass_by.remove(start)
    while pass_by:
        nearest = min(pass_by, key=lambda x: distance(path[-1], x))
        path.append(nearest)
        pass_by.remove(nearest)
    return path


def nearest(points, start):
    return min(points, key=lambda x: distance(start, x))


def sort_by_clockwise(points):
    """
    Sort point in a rotation order. Works in 2d but supports 3d.

    https://stackoverflow.com/questions/58377015/counterclockwise-sorting-of-x-y-data

    Args:
        points: List of points to sort in the form of [(x, y, z), (x, y,
        z)] or [(x, y), (x, y), (x, y), (x, y)]...

    Returns:
        list: List of tuples of coordinates sorted (2d or 3d).

    >>> sort_by_clockwise([(0, 45, 100), (4, -5, 5),(-5, 36, -2)])
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
    sorted_points = []
    for i in range(len(points)):
        j = 0
        while (x_sorted[i] != points[j][0]) and (y_sorted[i] != points[j][-1]):
            j += 1
        else:
            if len(points[0]) == 3:
                sorted_points.append((x_sorted[i], points[j][1], y_sorted[i]))
            else:
                sorted_points.append((x_sorted[i], y_sorted[i]))

    return sorted_points


def segments_intersection(line0, line1, full_line=True):
    """
    Find (or not) intersection between two lines. Works in 2d but
    supports 3d.

    https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines

    Args:
        line0 (tuple): Tuple of tuple of coordinates.
        line1 (tuple): Tuple of tuple of coordinates.
        full_line (bool, optional): True to find intersections along
        full line - not just in the segment.

    Returns:
        tuple: Coordinates (2d).

    >>> segments_intersection(((0, 0), (0, 5)), ((2.5, 2.5), (-2.5, 2.5)))
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

    if not full_line:
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
            if len(line0[0]) > 2:
                return middle_point(nearest(discrete_segment(line1[0], line1[1], pixel_perfect=True), (x, y)), nearest(discrete_segment(line0[0], line0[1], pixel_perfect=True), (x, y)))
            else:
                return x, y
        else:
            return None
    else:
        if len(line0[0]) > 2:
            return middle_point(nearest(discrete_segment(line1[0], line1[1], pixel_perfect=True), (x, y)), nearest(discrete_segment(line0[0], line0[1], pixel_perfect=True), (x, y)))
        else:
            return x, y


def circle_segment_intersection(
    circle_center, circle_radius, xy0, xy1, full_line=True, tangent_tolerance=1e-9
):
    """
    Find the points at which a circle intersects a line-segment. This
    can happen at 0, 1, or 2 points. Works in 2d but supports 3d.

    https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
    Note: We follow: http://mathworld.wolfram.com/Circle-LineIntersection.html

    Args:
        circle_center (tuple): The (x, y) location of the circle center.
        circle_radius (int): The radius of the circle.
        xy0 (tuple): The (x, y) location of the first point of the
        segment.
        xy1 ([tuple]): The (x, y) location of the second point of the
        segment.
        full_line (bool, optional): True to find intersections along
        full line - not just in the segment.  False will just return
        intersections within the segment. Defaults to True.
        tangent_tolerance (float, optional): Numerical tolerance at which we
        decide the intersections are close enough to consider it a
        tangent. Defaults to 1e-9.

    Returns:
        list: A list of length 0, 1, or 2, where each element is a point
        at which the circle intercepts a line segment (2d).
    """

    (p1x, p1y), (p2x, p2y), (cx, cy) = (
        (xy0[0], xy0[-1]),
        (xy1[0], xy1[-1]),
        (circle_center[0], circle_center[-1]),
    )
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** 0.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

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
            not full_line
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
            len(intersections) == 2 and abs(discriminant) <= tangent_tolerance
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
    (x1, y1) = xy1[0], xy1[-1]
    (x2, y2) = xy2[0], xy2[-1]
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


def curved_corner_intersection(
    line0, line1, start_distance, angle_adaptation=False, full_line=True, center=(), output_only_points=True
):
    """
    Create points between the two lines to smooth the intersection.

    Args:
        line0 (tuple): Tuple of tuple. Line coordinates. Order matters.
        line1 (tuple): Tuple of tuple. Line coordinates. Order matters.
        start_distance (int): distance from the intersection where the
        curve should starts.
        angleAdaptation (bool, optional): True will adapt the
        start_distance depending of the angle between the two lines.
        False will force the distance to be start_distance. Defaults to
        False.

    Returns:
        [list]: List of tuple of coordinates (2d) that forms the curve.
        Starts on the line and end on the other line.

    >>> curved_corner_intersection(((0, 0), (50, 20)), ((-5, 50), (25, -5)), 10)
    """
    print("\nInput:")
    print(line0, line1)
    intersection = segments_intersection(line0, line1, full_line)

    if intersection == None:
        return None

    # Define automatically the distance from the intersection, where the curve
    # starts.
    if angle_adaptation:
        angle = get_angle(
            (line0[0][0], line0[0][-1]),
            intersection,
            (line1[0][0], line1[0][-1]),
        )
        # Set here the radius of the circle for a square angle.
        start_distance = start_distance * abs(1 / (angle / 90))

    start_curve_point = circle_segment_intersection(
        intersection, start_distance, line0[0], intersection, full_line
    )[0]
    start_curve_point = (
        round(start_curve_point[0]), round(start_curve_point[-1]))
    end_curve_point = circle_segment_intersection(
        intersection, start_distance, line1[0], intersection, full_line
    )[0]
    end_curve_point = (round(end_curve_point[0]), round(end_curve_point[-1]))
    # Higher value for better precision
    perpendicular0 = perpendicular(10e3, start_curve_point, intersection)[0]
    perpendicular1 = perpendicular(10e3, end_curve_point, intersection)[-1]

    if center == ():
        center = segments_intersection(
            (perpendicular0, start_curve_point), (perpendicular1, end_curve_point)
        )
        center = round(center[0]), round(center[-1])

    # Distance with startCurvePoint and endCurvePoint from the center are the
    # same.
    radius = round(distance(start_curve_point, center))

    if output_only_points:
        circle_data = circle_points(
            center, radius, 32
        )  # n=round((2 * pi * radius) / 32)
    else:
        circle_data = circle(center, radius)[0]

    # Find the correct point on the circle.
    curved_corner_points_temporary = [start_curve_point]
    for point in circle_data:
        if is_in_triangle(point, intersection, start_curve_point, end_curve_point):
            curved_corner_points_temporary.append(
                (round(point[0]), round(point[1])))
    if output_only_points:
        curved_corner_points_temporary.append(end_curve_point)

    # Be sure that all the points are in correct order.
    curve_corner_points = optimized_path(
        curved_corner_points_temporary, start_curve_point)
    return curve_corner_points, center, radius
