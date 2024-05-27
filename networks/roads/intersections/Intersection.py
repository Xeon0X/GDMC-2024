from networks.geometry.segment_tools import parallel, orthogonal
from networks.geometry.point_tools import sort_by_clockwise, segments_intersection
from networks.roads import Road


class Intersection:
    def __init__(self, center, coordinates, Roads):
        self.center = center
        self.coordinates = coordinates
        self.Roads = Roads
        self.parallel_delimitations = []
        self.orthogonal_delimitations = []
        self.intersections = []

    def compute_curved_corner(self):
        # Necessary to test nearby intersection
        self.coordinates = sort_by_clockwise(self.coordinates)

        for i, coordinate in enumerate(self.coordinates):
            right_side, left_side = parallel((coordinate, self.center), self.Roads[i].width), parallel(
                (coordinate, self.center), -self.Roads[i].width)
            self.parallel_delimitations.append((right_side, left_side))
            self.orthogonal_delimitations.append(
                ((right_side[0], left_side[0]), (right_side[-1], left_side[-1])))

        for j in range(len(self.Roads)):
            self.intersections.append(segments_intersection(
                self.parallel_delimitations[j][1], self.parallel_delimitations[(j+1) % len(self.Roads)][0], full_line=False))

        print(self.intersections)
