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

    def compute_surface_perpendicular(self, width, normals):
        self.offset_left = curve.offset(self.curve, width, normals)
        self.offset_right = curve.offset(self.curve, -width, normals)
        self.perpendicular_segment = []

        for i in range(len(self.offset_left)):
            self.perpendicular_segment.append(segment.discrete_segment(
                self.offset_left[i], self.offset_right[i], pixel_perfect=False))

        self.surface = []

        for i in range(len(self.perpendicular_segment)-1):
            self.surface.append([])
            for j in range(len(self.perpendicular_segment[i])):
                # Hypothesis
                max_length_index = i
                min_length_index = i+1
                proportion = len(
                    self.perpendicular_segment[min_length_index])/len(self.perpendicular_segment[max_length_index])

                # Reverse order if wrong hypothesis
                if proportion > 1:
                    max_length_index = i+1
                    min_length_index = i
                    proportion = len(
                        self.perpendicular_segment[min_length_index])/len(self.perpendicular_segment[max_length_index])

                self.surface[i].append([])
                for k in range(len(self.perpendicular_segment[max_length_index])-1):
                    self.surface[i][j].append(segment.discrete_segment(
                        self.perpendicular_segment[max_length_index][k], self.perpendicular_segment[min_length_index][round(k * proportion)], pixel_perfect=False))

    def compute_surface_parallel(self, inner_range, outer_range, resolution, normals):
        self.left_side = []
        self.right_side = []
        for current_range in range(inner_range * resolution, outer_range * resolution):
            self.left_side.append(curve.offset(
                self.curve, current_range/resolution, normals))
            self.right_side.append(curve.offset(
                self.curve, -current_range/resolution, normals))
