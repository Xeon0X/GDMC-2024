import numpy as np
import networks.Segment as segment
from scipy import interpolate
from math import sqrt


def curve(target_points, resolution=40):
    """
    Returns a list of spaced points that approximate a smooth curve following target_points.

    https://stackoverflow.com/questions/18962175/spline-interpolation-coefficients-of-a-line-curve-in-3d-space
    """
    # Remove duplicates. Curve can't intersect itself
    points = tuple(map(tuple, np.array(target_points)))
    points = sorted(set(points), key=points.index)

    # Change coordinates structure to (x1, x2, x3, ...), (y1, y2, y3, ...) (z1, z2, z3, ...)
    coords = np.array(points, dtype=np.float32)
    x = coords[:, 0]
    y = coords[:, 1]
    z = coords[:, 2]

    # Compute
    tck, u = interpolate.splprep([x, y, z], s=3, k=2)
    x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
    u_fine = np.linspace(0, 1, resolution)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    x_rounded = np.round(x_fine).astype(int)
    y_rounded = np.round(y_fine).astype(int)
    z_rounded = np.round(z_fine).astype(int)

    return [(x, y, z) for x, y, z in zip(
        x_rounded, y_rounded, z_rounded)]


def curvature(curve):
    """Get the normal vector at each point of the given points representing the direction in wich the curve is turning.

    https://stackoverflow.com/questions/28269379/curve-curvature-in-numpy

    Args:
        curve (np.array): array of points representing the curve

    Returns:
        np.array: array of points representing the normal vector at each point in curve array

    >>> curvature(np.array(([0, 0, 0], [0, 0, 1], [1, 0, 1])))
    [[ 0.92387953 0. -0.38268343]
    [ 0.70710678 0. -0.70710678]
    [ 0.38268343 0. -0.92387953]]
    """
    curve_points = np.array(curve)
    dx_dt = np.gradient(curve_points[:, 0])
    dy_dt = np.gradient(curve_points[:, 1])
    dz_dt = np.gradient(curve_points[:, 2])
    velocity = np.array([[dx_dt[i], dy_dt[i], dz_dt[i]]
                        for i in range(dx_dt.size)])

    ds_dt = np.sqrt(dx_dt * dx_dt + dy_dt * dy_dt + dz_dt * dz_dt)

    tangent = np.array([1/ds_dt]).transpose() * velocity
    tangent_x = tangent[:, 0]
    tangent_y = tangent[:, 1]
    tangent_z = tangent[:, 2]

    deriv_tangent_x = np.gradient(tangent_x)
    deriv_tangent_y = np.gradient(tangent_y)
    deriv_tangent_z = np.gradient(tangent_z)

    dT_dt = np.array([[deriv_tangent_x[i], deriv_tangent_y[i], deriv_tangent_z[i]]
                     for i in range(deriv_tangent_x.size)])
    length_dT_dt = np.sqrt(
        deriv_tangent_x * deriv_tangent_x + deriv_tangent_y * deriv_tangent_y + deriv_tangent_z * deriv_tangent_z + 0.0001)

    normal = np.array([1/length_dT_dt]).transpose() * dT_dt
    return normal


def offset(curve, distance, normals):
    if len(normals) != len(curve):
        raise ValueError(
            'Number of normals and number of points in the curve do not match')

    # Offsetting
    offset_segments = [segment.parallel(
        (curve[i], curve[i+1]), distance, normals[i]) for i in range(len(curve) - 1)]

    # Combining segments
    combined_curve = []
    combined_curve.append(np.round(offset_segments[0][0]).tolist())
    for i in range(0, len(offset_segments)-1):
        combined_curve.append(segment.middle_point(
            offset_segments[i][1], offset_segments[i+1][0]))
    combined_curve.append(np.round(offset_segments[-1][1]).tolist())

    return combined_curve


def resolution_distance(target_points, spacing_distance):
    length = 0
    for i in range(len(target_points) - 1):
        length += sqrt(
            ((target_points[i][0] - target_points[i + 1][0]) ** 2)
            + ((target_points[i][1] - target_points[i + 1][1]) ** 2)
            + ((target_points[i][2] - target_points[i + 1][2]) ** 2)
        )
    return round(length / spacing_distance), length


def simplify_segments(points, epsilon):
    if len(points) < 3:
        return points

    # Find the point with the maximum distance
    max_distance = 0
    max_index = 0
    end_index = len(points) - 1

    for i in range(1, end_index):
        distance = get_distance(points[i], points[0])
        if distance > max_distance:
            max_distance = distance
            max_index = i

    simplified_points = []

    # If the maximum distance is greater than epsilon, recursively simplify
    if max_distance > epsilon:
        rec_results1 = simplify_segments(points[:max_index+1], epsilon)
        rec_results2 = simplify_segments(points[max_index:], epsilon)

        # Combine the simplified sub-results
        simplified_points.extend(rec_results1[:-1])
        simplified_points.extend(rec_results2)
    else:
        # The maximum distance is less than epsilon, retain the endpoints
        simplified_points.append(points[0])
        simplified_points.append(points[end_index])

    return simplified_points
