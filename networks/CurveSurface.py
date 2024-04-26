import networks.Curve as curve
import networks.Segment as segment
import numpy as np


class CurveSurface:
    def __init__(self, points, reshape=True, spacing_distance=10):
        self.points = np.array(points)
        if reshape:
            self.resolution, self.length = curve.resolution_distance(
                self.points, spacing_distance=spacing_distance)
            self.curve = curve.curve(self.points, self.resolution)
        else:  # Point can also be given already in curved form
            self.curve = self.points

    def compute_curvature(self):
        self.curvature = curve.curvature(self.curve)

    def compute_surface(self, width, normals, resolution):
        self.offset_points = [None] * (width * resolution)
        self.surface = []
        for line_range in range(width * resolution):
            self.offset_points[line_range] = curve.offset(
                self.curve, line_range/resolution, normals)

            for i in range(len(self.offset_points[line_range])-1):
                self.surface.extend(segment.discrete_segment(
                    self.offset_points[line_range][i], self.offset_points[line_range][i+1], pixel_perfect=False))

        print(self.surface)
