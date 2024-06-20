from math import inf, sqrt
from typing import List, Tuple, Union

import numpy as np

from networks.geometry.Circle import Circle
from networks.geometry.Point2D import Point2D
from networks.geometry.Segment2D import Segment2D


class Polyline:
    def __init__(self, points: List[Point2D]):
        """A polyline with smooth corners, only composed of segments and circle arc.

        Mathematics and algorithms behind this can be found here: https://cdr.lib.unc.edu/concern/dissertations/pz50gw814?locale=en, E2 Construction of arc roads from polylines, page 210.

        Args:
            points (List[Point2D]): List of 2d-points in order describing the polyline.

        Raises:
            ValueError: At least 4 points required.

        >>> Polyline((Point2D(0, 0), Point2D(0, 10), Point2D(50, 10), Point2D(20, 20)))
        """
        self.output_points = points
        self.points_array = Point2D.to_arrays(
            self._remove_collinear_points(points))
        self.length_polyline = len(self.points_array)

        if self.length_polyline < 4:
            print(self.length_polyline)
            print(self.points_array)
            print(self.output_points)
            raise ValueError("The list must contain at least 4 elements.")

        self.vectors = [None] * self.length_polyline  # v
        self.lengths = [0] * (self.length_polyline - 1)  # l
        self.unit_vectors = [None] * self.length_polyline  # n
        self.tangente = [0] * self.length_polyline  # f

        # alpha, maximum radius factor
        self.alpha_radii = [0] * self.length_polyline

        # Useful outputs. In order to not break indexation, each list has the same length, even if for n points, there is n-2 radius.
        # Lists will start and end with None.
        self.radii = [0] * self.length_polyline  # r, list of points
        self.centers = [None] * self.length_polyline  # c, list of points
        # list of tuple of points (first intersection, corresponding corner, last intersection)
        self.acrs_intersections = [None] * self.length_polyline
        self.arcs = [[] for _ in range(self.length_polyline)]  # list of points
        # self.bisectors = [None] * self.length_polyline

        # For n points, there is n-1 segments. Last element should stays None.
        self.segments = [None] * \
            self.length_polyline  # list of segments

        # Run procedure
        self._compute_requirements()
        self._compute_alpha_radii()

        self._alpha_assign(0, self.length_polyline-1)
        self.get_radii()
        self.get_centers()
        self.get_arcs_intersections()
        self.get_arcs()
        self.get_segments()

        self.total_line_output = []
        for i in range(1, self.length_polyline-1):
            self.total_line_output.extend(self.segments[i].segment())
            self.total_line_output.extend(self.arcs[i])
        self.total_line_output.extend(
            self.segments[self.length_polyline-1].segment())

        self.total_line_output = self.total_line_output[0].optimized_path(
            self.total_line_output)

    def __repr__(self):
        return str(self.alpha_radii)

    def get_radii(self) -> List[Union[int]]:
        for i in range(1, self.length_polyline-1):
            self.radii[i] = round(self.alpha_radii[i] * self.tangente[i])
        return self.radii

    def get_centers(self) -> List[Union[Point2D, None]]:
        for i in range(1, self.length_polyline-1):
            bisector = (self.unit_vectors[i] - self.unit_vectors[i-1]) / (
                np.linalg.norm(self.unit_vectors[i] - self.unit_vectors[i-1]))

            array = self.points_array[i] + sqrt((self.radii[i]
                                                 ** 2) + (self.alpha_radii[i] ** 2)) * bisector
            self.centers[i] = Point2D(array[0], array[1]).round()
        return self.centers

    def get_arcs_intersections(self) -> List[Tuple[Point2D]]:
        """Get arcs intersections points.

        First and last elements elements of the list should be None. For n points, there are n-1 segments, and n-2 angle.

        Returns:
            list[tuple(Point2D)]: List of tuples composed - in order - of the first arc points, the corner points, the last arc points. The corresponding arc circle is inside this triangle.
        """
        for i in range(1, self.length_polyline-1):

            point_1 = Point2D.from_arrays(self.points_array[i] -
                                          self.alpha_radii[i] * self.unit_vectors[i-1])
            point_2 = Point2D.from_arrays(self.points_array[i] +
                                          self.alpha_radii[i] * self.unit_vectors[i])

            # If Arc intersection are near, meaning no segment between, we need to remove error due to discrete appoximation.
            # Instead of two independant arc intersection, we make sure to combine both.
            if i > 1:
                if point_1.distance(self.acrs_intersections[i-1][2]) <= 2:
                    middle = Segment2D(
                        self.centers[i], self.centers[i-1]).middle_point()
                    combined = Segment2D(
                        point_1, self.acrs_intersections[i-1][2]).middle_point()

                    # To correct mis-alignement bewteen center 1 - arc intersection 1 and 2 combined - center 2
                    if middle.distance(combined) <= 2:
                        point_1 = middle
                        self.acrs_intersections[i-1][2] = middle
                    else:
                        point_1 = combined
                        self.acrs_intersections[i-1][2] = combined

            self.acrs_intersections[i] = [point_1.round(), Point2D.from_arrays(
                self.points_array[i]), point_2.round()]
        return self.acrs_intersections

    def get_arcs(self) -> List[Point2D]:
        for i in range(1, self.length_polyline-1):
            points = Circle(self.centers[i]).circle(self.radii[i])

            # Better to do here than drawing circle arc inside big triangle!
            double_point_a = Point2D.from_arrays(Point2D.to_arrays(self.acrs_intersections[i][0]) + 5 * (Point2D.to_arrays(
                self.acrs_intersections[i][0]) - Point2D.to_arrays(self.centers[i])))
            double_point_b = Point2D.from_arrays(Point2D.to_arrays(self.acrs_intersections[i][2]) + 5 * (Point2D.to_arrays(
                self.acrs_intersections[i][2]) - Point2D.to_arrays(self.centers[i])))

            for j in range(len(points)):
                if points[j].is_in_triangle(double_point_a, self.centers[i], double_point_b):
                    self.arcs[i].append(points[j])
        return self.arcs

    def get_segments(self) -> List[Segment2D]:
        """Get the segments between the circle arcs and at the start and end.

        Last list element should be None, and last usable index is -2 or self.length_polyline - 2. For n points, there are n-1 segments.

        Returns:
            list[Segment2D]: List of segments in order.
        """
        # Get first segment.
        # First arc index is 1 because index 0 is None due to fix list lenght.  Is it a good choice?
        self.segments[1] = Segment2D(Point2D.from_arrays(
            self.points_array[0]), self.acrs_intersections[1][0])

        # Get segments between arcs
        for i in range(2, self.length_polyline - 1):
            self.segments[i] = Segment2D(Point2D(
                self.acrs_intersections[i-1][2].x, self.acrs_intersections[i-1][2].y), Point2D(self.acrs_intersections[i][0].x, self.acrs_intersections[i][0].y))

        # Why -3?
        # For n points, there are n-1 segments.
        self.segments[-1] = Segment2D(self.acrs_intersections[-2][2], Point2D.from_arrays(
            self.points_array[-1]))

        return self.segments

    def _alpha_assign(self, start_index: int, end_index: int):
        """
        The alpha-assign procedure assigning radii based on a polyline.
        """
        minimum_radius, minimum_index = inf, end_index

        if start_index + 1 >= end_index:
            return

        alpha_b = min(
            self.lengths[start_index] - self.alpha_radii[start_index], self.lengths[start_index + 1])
        current_radius = max(self.tangente[start_index] * self.alpha_radii[start_index],
                             # Radius at initial segment
                             self.tangente[start_index + 1] * alpha_b)

        if current_radius < minimum_radius:
            minimum_radius, minimum_index = current_radius, start_index
            # 0, 8
            alpha_low, alpha_high = self.alpha_radii[start_index], alpha_b

        for i in range(start_index + 1, end_index - 1):  # Radii for internal segments
            alpha_a, alpha_b, current_radius = self._radius_balance(i)

            if current_radius < minimum_radius:
                minimum_radius, minimum_index = current_radius, i
                alpha_low, alpha_high = alpha_a, alpha_b

        alpha_a = min(
            self.lengths[end_index-2], self.lengths[end_index-1]-self.alpha_radii[end_index])

        current_radius = max(self.tangente[end_index-1]*alpha_a, self.tangente[end_index]
                             # Radius at final segment
                             * self.alpha_radii[end_index])

        if current_radius < minimum_radius:
            minimum_radius, minimum_index = current_radius, end_index - 1
            alpha_low, alpha_high = alpha_a, self.alpha_radii[end_index]

        # Assign alphas at ends of selected segment
        self.alpha_radii[minimum_index] = alpha_low
        self.alpha_radii[minimum_index+1] = alpha_high
        # Recur on lower segments
        self._alpha_assign(start_index, minimum_index)
        # Recur on higher segments
        self._alpha_assign(minimum_index + 1, end_index)

    def _radius_balance(self, i: int):
        """
        Returns the radius that balances the radii on either end segement i.
        """
        alpha_a = min(self.lengths[i-1], (self.lengths[i] *
                      self.tangente[i+1])/(self.tangente[i] + self.tangente[i+1]))
        alpha_b = min(self.lengths[i+1], self.lengths[i]-alpha_a)
        return alpha_a, alpha_b, min(self.tangente[i]*alpha_a, self.tangente[i+1]*alpha_b)

    def _compute_requirements(self):
        # Between two points, there is only one segment
        for j in range(self.length_polyline-1):
            self.vectors[j] = self.points_array[j+1] - self.points_array[j]
            self.lengths[j] = np.linalg.norm(self.vectors[j])
            self.unit_vectors[j] = self.vectors[j]/self.lengths[j]

        # Between two segments, there is only one angle
        for i in range(1, self.length_polyline-1):
            dot = np.dot(self.unit_vectors[i], self.unit_vectors[i-1])
            self.tangente[i] = sqrt((1+dot)/(1-dot))
            # self.bisectors[i] = (self.unit_vectors[i]+self.unit_vectors[i-1]) / \
            #     np.linalg.norm(self.unit_vectors[i]-self.unit_vectors[i-1])

    def _compute_alpha_radii(self):
        self.alpha_radii[0] = 0
        self.alpha_radii[self.length_polyline-1] = 0

    @staticmethod
    def _remove_collinear_points(points):
        output_points = [points[0]]

        for i in range(1, len(points) - 1):
            if not Point2D.collinear(
                    points[i-1], points[i], points[i+1]):
                output_points.append(points[i])

        output_points.append(points[-1])
        return output_points
