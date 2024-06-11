from math import sqrt, cos, pi, sin
import numpy as np
from networks.geometry.segment_tools import discrete_segment, middle_point, parallel


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
    return (x3, y3), (x4, y4)


def curved_corner_by_distance(
    intersection, xyz0, xyz1, distance_from_intersection, resolution, full_line=True
):
    # Compute the merging point on the first line
    start_curve_point_d1 = circle_segment_intersection(
        intersection, distance_from_intersection, xyz0, intersection, full_line
    )[0]
    start_curve_point_d1 = (
        round(start_curve_point_d1[0]), nearest(discrete_segment(intersection, xyz0), (start_curve_point_d1[0], 100, start_curve_point_d1[-1]))[1], round(start_curve_point_d1[-1]))

    # Compute the merging point on the second line
    end_curve_point_d1 = circle_segment_intersection(
        intersection, distance_from_intersection, xyz1, intersection, full_line
    )[0]
    end_curve_point_d1 = (
        round(end_curve_point_d1[0]), nearest(discrete_segment(intersection, xyz1), (end_curve_point_d1[0], 100, end_curve_point_d1[-1]))[1], round(end_curve_point_d1[-1]))

    # Compute the merging point on the first line
    start_curve_point_d2 = circle_segment_intersection(
        (intersection[0], intersection[1]), distance_from_intersection, (
            xyz0[0], xyz0[1]), (intersection[0], intersection[1]), full_line
    )[0]
    start_curve_point_d2 = (
        round(start_curve_point_d2[0]), round(start_curve_point_d2[1]), nearest(discrete_segment(intersection, xyz0), (start_curve_point_d1[0], start_curve_point_d2[-1], 100))[-1])

    # Compute the merging point on the second line
    end_curve_point_d2 = circle_segment_intersection(
        (intersection[0], intersection[1]
         ), distance_from_intersection, (xyz1[0], xyz1[1]), (intersection[0], intersection[1]), full_line
    )[0]
    end_curve_point_d2 = (
        round(end_curve_point_d2[0]), round(end_curve_point_d2[-1]), nearest(discrete_segment(
            intersection, xyz1), (end_curve_point_d2[0], end_curve_point_d2[-1], 100))[-1])

    # Compute the intersection between perpendicular lines at the merging points
    # Higher value for better precision
    perpendicular0_d1 = perpendicular(
        10e3, start_curve_point_d1, intersection)[0]
    perpendicular0_d1 = (
        round(perpendicular0_d1[0]), round(perpendicular0_d1[-1]))
    perpendicular1_d1 = perpendicular(
        10e3, end_curve_point_d1, intersection)[1]
    perpendicular1_d1 = (
        round(perpendicular1_d1[0]), round(perpendicular1_d1[-1]))

    perpendicular0_d2 = perpendicular(
        10e3, (start_curve_point_d1[0], start_curve_point_d1[1]), (intersection[0], intersection[1]))[0]
    perpendicular0_d2 = (
        round(perpendicular0_d2[0]), round(perpendicular0_d2[1]))
    perpendicular1_d2 = perpendicular(
        10e3, (end_curve_point_d1[0], end_curve_point_d1[1]), (intersection[0], intersection[1]))[1]
    perpendicular1_d2 = (
        round(perpendicular1_d2[0]), round(perpendicular1_d2[1]))

    # Centers
    center_d1 = segments_intersection(
        (perpendicular0_d1, start_curve_point_d1), (perpendicular1_d1, end_curve_point_d1))
    center_d1 = round(center_d1[0]), middle_point(
        xyz0, xyz1)[1], round(center_d1[-1])

    center_d2 = segments_intersection(
        (perpendicular0_d2, (start_curve_point_d1[0], start_curve_point_d1[1])), (perpendicular1_d2, (end_curve_point_d1[0], end_curve_point_d1[1])))
    center_d2 = round(center_d2[0]), round(center_d2[1]), middle_point(
        xyz0, xyz1)[-1]

    # Compute the curvature for indications
    curvature_d1 = round(distance(start_curve_point_d1, center_d1))
    curvature_d2 = round(
        distance((start_curve_point_d1[0], start_curve_point_d1[1]), center_d2))

    # Return a full discrete circle or only some points of it
    if resolution != 0:
        circle_data_d1 = circle_points(
            center_d1, curvature_d1, resolution
        )
        circle_data_d2 = circle_points(
            center_d2, curvature_d2, resolution
        )
    else:
        circle_data_d1 = circle(center_d1, curvature_d1)[0]
        circle_data_d2 = circle(center_d2, curvature_d2)[0]

    # Find the correct points on the circle.
    curved_corner_points_temporary_d1 = [start_curve_point_d1]
    for point in circle_data_d1:
        if is_in_triangle(point, intersection, start_curve_point_d1, end_curve_point_d1):
            curved_corner_points_temporary_d1.append(point)
    curved_corner_points_temporary_d1.append(end_curve_point_d1)

    # Be sure that all the points are in correct order.
    curve_corner_points_d1 = optimized_path(
        curved_corner_points_temporary_d1, start_curve_point_d1)

    # On the other axis
    curved_corner_points_temporary_d2 = [
        (start_curve_point_d1[0], start_curve_point_d1[1])]
    for point in circle_data_d2:

        if is_in_triangle(point, (intersection[0], intersection[1]), (start_curve_point_d1[0], start_curve_point_d1[1]), (end_curve_point_d1[0], end_curve_point_d1[1])):
            curved_corner_points_temporary_d2.append(point)
    curved_corner_points_temporary_d2.append(
        (end_curve_point_d1[0], end_curve_point_d1[1]))

    # Be sure that all the points are in correct order.
    curve_corner_points_d2 = optimized_path(
        curved_corner_points_temporary_d2, (start_curve_point_d1[0], start_curve_point_d1[1]))

    # Determine driving axis
    if len(curve_corner_points_d1) <= len(curve_corner_points_d2):
        main_points = curve_corner_points_d2
        projected_points = curve_corner_points_d1
    else:
        main_points = curve_corner_points_d1
        projected_points = curve_corner_points_d2

    print("Main\n")
    print(main_points)
    print("Projected\n")
    print(projected_points)

    curve_corner_points = []
    for i in range(len(main_points)):
        y = projected_points[round(
            i * (len(projected_points)-1)/len(main_points))][-1]
        curve_corner_points.append((round(main_points[i][0]), round(
            y), round(main_points[i][-1])))
    return curve_corner_points, center_d1, curvature_d1, center_d2, curvature_d2


def curved_corner_by_curvature(
    intersection, xyz0, xyz1, curvature_radius, resolution, full_line=True
):
    # 3d support limited to linear interpollation on the y axis.
    print(xyz0, intersection, xyz1)
    # Get the center.
    center = segments_intersection(parallel(
        (xyz0, intersection), -curvature_radius), parallel((xyz1, intersection), curvature_radius))
    center = round(center[0]), round(center[-1])

    # Return a full discrete circle or only some points of it.
    if resolution != 0:
        circle_data = circle_points(
            center, curvature_radius, resolution
        )
    else:
        circle_data = circle(center, curvature_radius)[0]

    # Compute the merging point on the first line.
    print(center, curvature_radius, xyz0, intersection)
    start_curve_point = circle_segment_intersection(
        center, curvature_radius, xyz0, intersection, full_line
    )[0]
    start_curve_point = (
        round(start_curve_point[0]), round(start_curve_point[-1]))

    # Compute the merging point on the second line.
    end_curve_point = circle_segment_intersection(
        center, curvature_radius, xyz1, intersection, full_line
    )[0]
    end_curve_point = (
        round(end_curve_point[0]), round(end_curve_point[-1]))

    # Find the correct points on the circle.
    curved_corner_points_temporary = [start_curve_point]
    for point in circle_data:
        # print(point, intersection, start_curve_point, end_curve_point, is_in_triangle(
        #     point, intersection, start_curve_point, end_curve_point))
        # if is_in_triangle(point, intersection, start_curve_point, end_curve_point):
        curved_corner_points_temporary.append(
            (round(point[0]), round(point[1])))
    curved_corner_points_temporary.append(end_curve_point)

    # Be sure that all the points are in correct order.
    curve_corner_points = optimized_path(
        curved_corner_points_temporary, start_curve_point)

    # Distance from intersection just for information
    distance_from_intersection = round(distance(start_curve_point, center))
    return curve_corner_points, center, distance_from_intersection, parallel(
        (xyz0, intersection), -curvature_radius), parallel((xyz1, intersection), curvature_radius)


def coordinates_to_vectors(coordinates):
    vectors = []
    for coordinate in coordinates:
        vectors.append(np.array(coordinate.coordinate))

    if (len(vectors) == 1):
        return vectors[0]
    else:
        return vectors
