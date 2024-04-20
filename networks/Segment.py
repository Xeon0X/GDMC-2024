import numpy as np


def parallel(segment, distance, normal=np.array([0, 1, 0])):
    """Get parallel segment in 3D space at a distance.

    Args:
        segment (np.array, np.array): start and end points of the segement.
        distance (int): distance between both segment. Thickness in the context of a line. Positive direction means left.

    Returns:
        (np.array(), np.array()): parallel segment.

    >>> parrallel(((0, 0, 0), (0, 0, 10)), 10))
    (array([-10.,   0.,   0.]), array([-10.,   0.,  10.]))
    """
    return (orthogonal(segment[0], segment[1], distance, normal), orthogonal(segment[1], segment[0], -distance, normal))


def normalized(vector):
    magnitude = np.linalg.norm(vector)
    normalized_vector = vector / magnitude
    return normalized_vector


def orthogonal(origin, point, distance, normal=np.array([0, 1, 0])):
    """Get orthogonal point from a given one at the specified distance in 3D space with normal direction.

    Args:
        origin (tuple or np.array): origin
        point (tuple or np.array): (point-origin) makes the first vector. Only the direction is used.
        distance (int): distance from the origin. Thickness in the context of a line. Positive direction means left.
        normal (list or np.array, optional): second vector. Defaults to the vertical [0, 1, 0].

    Raises:
        ValueError: if vectors are not linearly independent.

    Returns:
        np.array: (x y z)

    >>> orthogonal((5, 5, 5), (150, 5, 5), 10)
    [ 5.  5. 15.]
    """
    vector = np.subtract(point, origin)
    normalized_vector = normalized(vector)
    normalized_normal = normalized(normal)
    orthogonal = np.cross(normalized_vector, normalized_normal)

    if np.array_equal(orthogonal, np.zeros((3,))):
        raise ValueError("The input vectors are not linearly independent.")

    orthogonal = np.add(np.multiply(orthogonal, distance), origin)
    return orthogonal


def discrete_segment(xyz1, xyz2, pixel_perfect=True):
    """
    Calculate a line between two points in 3D space.

    https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/

    Args:
        xyz1 (tuple): First coordinates.
        xyz2 (tuple): Second coordinates.
        pixel_perfect (bool, optional): If true, remove unnecessary coordinates connecting to other coordinates side by side, leaving only a diagonal connection. Defaults to True.

    Returns:
        list: List of coordinates.
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

    points = []
    points.append((x1, y1, z1))
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
            points.append((x1, y1, z1))
            if p1 >= 0:
                y1 += ys
                if not pixel_perfect:
                    if points[-1][1] != y1:
                        points.append((x1, y1, z1))
                p1 -= 2 * dx
            if p2 >= 0:
                z1 += zs
                if not pixel_perfect:
                    if points[-1][2] != z1:
                        points.append((x1, y1, z1))
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz

    # Driving axis is Y-axis
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y1 != y2:
            y1 += ys
            points.append((x1, y1, z1))
            if p1 >= 0:
                x1 += xs
                if not pixel_perfect:
                    if points[-1][0] != x1:
                        points.append((x1, y1, z1))
                p1 -= 2 * dy
            if p2 >= 0:
                z1 += zs
                if not pixel_perfect:
                    if points[-1][2] != z1:
                        points.append((x1, y1, z1))
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz

    # Driving axis is Z-axis
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z1 != z2:
            z1 += zs
            points.append((x1, y1, z1))
            if p1 >= 0:
                y1 += ys
                if not pixel_perfect:
                    if points[-1][1] != y1:
                        points.append((x1, y1, z1))
                p1 -= 2 * dz
            if p2 >= 0:
                x1 += xs
                if not pixel_perfect:
                    if points[-1][0] != x1:
                        points.append((x1, y1, z1))
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
    return points
