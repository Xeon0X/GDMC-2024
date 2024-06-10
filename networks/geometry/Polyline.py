from typing import Type
from networks.geometry.Point2D import Point2D

from math import sqrt, inf
import numpy as np


class Polyline:
    def __init__(self, points: List[Point2D]):
        """A polyline with smooth corners, only composed of segments and circle arc.

        Mathematics and algorithms behind this can be found here: https://cdr.lib.unc.edu/concern/dissertations/pz50gw814?locale=en, E2 Construction of arc roads from polylines, page 210.

        Args:
            points (List[Point2D]): List of 2d-points in order describing the polyline.

        Raises:
            ValueError: At least 4 points required.
        """
        self.points = coordinates_to_vectors(points)
        self.length_polyline = len(points)

        if self.length_polyline < 4:
            raise ValueError("The list must contain at least 4 elements.")

        self.vectors = [None] * self.length_polyline
        self.lengths = [None] * self.length_polyline
        self.unit_vectors = [None] * self.length_polyline
        self.tangente = [None] * self.length_polyline

        self.alpha_radii = [None] * self.length_polyline

        self._compute_requirements()
        self._compute_alpha_radii()

        _alpha_assign(0, self.length_polyline-1)

    def _alpha_assign(self, start_index, end_index):
        """
        The alpha-assign procedure assigning radii based on a polyline.
        """
        minimum_radius, minimum_index = inf, end_index

        if start_index + 1 >= end_index:
            return

        alpha_b = min(
            self.lengths[start_index] - self.alpha_radii[start_index], self.lengths[start_index + 1])
        current_radius = max(self.tangente[start_index] * self.alpha_radii[start_index],
                             self.tangente[start_index + 1] * alpha_b)  # Radis at initial segment

        if current_radius < minimum_radius:
            minimum_radius, minimum_index = current_radius, start_index
            alpha_low, alpha_high = self.alpha_radii[start_index], alpha_b

        for i in range(start_index + 1, end_index - 2):  # Radii for internal segments
            alpha_a, alpha_b, current_radius = self._radius_balance(i)
            if current_radius < minimum_radius:
                alpha_low, alpha_high = alpha_a, self.alpha_radii[end_index]

        # Assign alphas at ends of selected segment
        self.alpha_radii[minimum_index] = alpha_low
        self.alpha_radii[minimum_index+1] = alpha_high
        print(alpha_low, alpha_high)

        # Recur on lower segments
        self._alpha_assign(start_index, minimum_index)
        # Recur on higher segments
        self._alpha_assign(minimum_index + 1, end_index)

    def _radius_balance(self, i: int):
        """
        Returns the radius that balances the radii on either end segement i.
        """

        alpha_a = min(self.lengths[i-1], (self.lengths[i]*self.tangente[i+1]) /
                      (self.tangente[i] + self.tangente[i+1]))
        alpha_b = min(self.lengths[i+1], self.lengths[i]-alpha_a)

        return alpha_a, alpha_b, max(self.tangente[i]*alpha_a, self.tangente[i+1]*alpha_b)

    def _compute_requirements(self):
        # Between two points, there is only one segment
        for j in range(self.length_polyline-1):
            self.vectors[j] = self.points[j+1] - self.points[j]
            self.lengths[j] = np.linalg.norm(self.vectors[j])
            self.unit_vectors[j] = self.vectors[j]/self.lengths[j]

        # print("\n\n", vectors, "\n\n", lengths, "\n\n", unit_vectors, "\n\n")

        # Between two segments, there is only one angle
        for k in range(1, self.length_polyline-1):
            cross = np.dot(self.unit_vectors[k], self.unit_vectors[k-1])
            self.tangente[k] = sqrt((1+cross)/(1-cross))

    def _compute_alpha_radii(self):
        self.alpha_radii[0] = 0
        self.alpha_radii[self.length_polyline-1] = 0

        for i in range(1, self.length_polyline-2):
            self.alpha_radii[i] = min(self.lengths[i-1] - self.alpha_radii[i-1], (self.lengths[i]
                                                                                  * self.tangente[i+1])/(self.tangente[i]+self.tangente[i+1]))


# polyline = Polyline((Point2D(0, 9), Point2D(0, 10), Point2D(
#     10, 10), Point2D(10, 20), Point2D(20, 20), Point2D(20, 30), Point2D(60, 60), Point2D(-60, -60)))

polyline = Polyline((Point2D(0, 10), Point2D(-10, -10),
                    Point2D(20, 0), Point2D(20, 20)))


# print(polyline.radius_balance(2))

polyline._alpha_assign(1, polyline.length_polyline-1)
print(polyline.alpha_radii)
