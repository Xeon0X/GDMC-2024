from math import sqrt, inf
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


def coordinates_to_vectors(coordinates):
    vectors = []
    for coordinate in coordinates:
        vectors.append(np.array(coordinate.get_coordinates()))

    if (len(vectors) == 1):
        return vectors[0]
    else:
        return vectors


class Polyline:
    def __init__(self, points):
        self.points = coordinates_to_vectors(points)
        self.length_polyline = len(points)

        self.vectors = [None] * self.length_polyline
        self.lengths = [None] * self.length_polyline
        self.unit_vectors = [None] * self.length_polyline
        self.tangente = [None] * self.length_polyline

        self.compute_requirements()

    def compute_requirements(self):

        # Between two points, there is only one segment
        for j in range(self.length_polyline-1):
            self.vectors[j] = self.points[j+1] - self.points[j]
            self.lengths[j] = np.linalg.norm(self.vectors[j])
            self.unit_vectors[j] = self.vectors[j]/self.lengths[j]

        # print("\n\n", vectors, "\n\n", lengths, "\n\n", unit_vectors, "\n\n")

        # Between two segments, there is only one angle
        for k in range(self.length_polyline-2):
            cross = np.dot(self.unit_vectors[k+1], self.unit_vectors[k])
            self.tangente[k] = sqrt((1+cross)/(1-cross))

    def radius_balance(self, i):
        """
        Returns the radius that balances the radii on either end segement i.
        """

        alpha_a = min(self.lengths[i], (self.lengths[i+1]*self.tangente[i+1]) /
                      (self.tangente[i] + self.tangente[i+1]))
        alpha_b = min(self.lengths[i+2], self.lengths[i+1]-alpha_a)

        return alpha_a, alpha_b, max(self.tangente[i]*alpha_a, self.tangente[i+1]*alpha_b)

    def alpha_assign(polyline, alpha_radii, start_index, end_index):
        """
        The Alpha-assign procedure assigning radii based on a polyline.
        """
        minimum_radius, minimum_index = inf, end_index

        if start_index + 1 >= end_index:
            return

        alpha_b = min(lenghts[start_index] -
                      alpha_radii[start_index], lenghts[start_index + 1])
        current_radius = max(tangente[start_index] * alpha_radii[start_index],
                             tangente[start_index + 1] * alpha_b)  # Radis at initial segment

        if current_radius < minimum_radius:
            minimum_radius, minimum_index = current_radius, start_index
            alpha_low, alpha_high = alpha_radii[start_index], alpha_b

        for i in range(start_index + 1, end_index - 2):  # Radii for internal segments
            alpha_a, alpha_b, current_radius = radius_balance(polyline, i)
            if current_radius < minimum_radius:
                alpha_low, alpha_high = alpha_a, alpha_radii[end_index]

        # Assign alphas at ends of selected segment
        alpha_radii[minimum_index] = alpha_low
        alpha_radii[minimum_index+1] = alpha_high
        # Recur on lower segments
        alpha_assign(alpha_radii, start_index, minimum_index)
        alpha_assign(alpha_radii, minimum_index + 1,
                     end_index)  # Recur on higher segments

    def compute_alpha_radii(polyline):
        length_array = len(polyline)
        apha_radii = [None] * length_array

        alpha_radii[0] = 0
        alpha_radii[length_array-1] = 0

        for i in range(1, length_array-2):
            alpha_radii[i] = min()


polyline = Polyline((Point2D(0, 0), Point2D(
    0, 10), Point2D(10, 10), Point2D(10, 20)))
print(polyline.radius_balance(0))
