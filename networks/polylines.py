from math import sqrt
import numpy as np


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x} {self.y})"

    def copy(self):
        return Point2D(self.x, self.y)

    def get_coordinates(self):
        return (self.x, self.y)


def radius_balance(polylines, i):
    """
    Returns the radius that balances the radii on either end segement i.
    """

    vectors = [None] * 3
    lengths = [None] * 3
    unit_vectors = [None] * 3
    tangente = [None] * 3

    for j in range(3):
        vectors[j] = polylines[i+j] - polylines[i+j-1]
        lengths[j] = np.linalg.norm(vectors[j])
        unit_vectors[j] = vectors[j]/lengths[j]

    print("\n\n", vectors, "\n\n", lengths, "\n\n", unit_vectors, "\n\n")

    for k in range(2):
        cross = np.dot(unit_vectors[k+1], unit_vectors[k])
        print(cross)
        tangente[k] = sqrt((1+cross)/(1-cross))
        print("\n", tangente[k])

    alpha_a = min(lengths[0], (lengths[1]*tangente[1]) /
                  (tangente[0] + tangente[1]))
    alpha_b = min(lengths[2], lengths[1]-alpha_a)

    return alpha_a, alpha_b, max(tangente[0]*alpha_a, tangente[1]*alpha_b)


def coordinates_to_vectors(coordinates):
    vectors = []
    for coordinate in coordinates:
        vectors.append(np.array(coordinate.get_coordinates()))

    if (len(vectors) == 1):
        return vectors[0]
    else:
        return vectors


polyline = coordinates_to_vectors(
    (Point2D(0, 0), Point2D(0, 10), Point2D(10, 10), Point2D(10, 20)))

print(radius_balance(polyline, 1))
