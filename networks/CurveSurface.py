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

    def compute_surface(self, width, normals):
        self.offset_left = curve.offset(self.curve, width, normals)
        self.offset_right = curve.offset(self.curve, -width, normals)
        self.perpendicular_segment = []

        for i in range(len(self.offset_left)):
            self.perpendicular_segment.append(segment.discrete_segment(
                self.offset_left[i], self.offset_right[i], pixel_perfect=False))

        self.surface = []

        for i in range(len(self.perpendicular_segment)-1):
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

                for k in range(len(self.perpendicular_segment[max_length_index])):
                    self.surface.extend(segment.discrete_segment(
                        self.perpendicular_segment[max_length_index][k], self.perpendicular_segment[min_length_index][round(k * proportion)-1], pixel_perfect=False))

        # for i in range(len(self.offset_points)):
        #     self.perpendicular_segment[i].append(
        #         segment.discrete_segment(self.offset_points[i], self.curve[i]))

        # for j in range(len(self.offset_points)-1):
        #     # Hypothesis
        #     max_length_index = j
        #     min_length_index = j+1
        #     proportion = len(
        #         self.perpendicular_segment[min_length_index])/len(self.perpendicular_segment[max_length_index])

        #     # Reverse order if wrong hypothesis
        #     if proportion > 1:
        #         max_length_index = j+1
        #         min_length_index = j
        #         proportion = len(
        #             self.perpendicular_segment[min_length_index])/len(self.perpendicular_segment[max_length_index])

        #     for k in range(len(self.perpendicular_segment[max_length_index])):
        #         # print(self.perpendicular_segment[max_length_index][k],
        #         #     self.perpendicular_segment[min_length_index][round(k * proportion)])
        #         self.surface.extend(segment.discrete_segment(
        #             self.perpendicular_segment[max_length_index][k], self.perpendicular_segment[min_length_index][round(k * proportion)]))

        # for line_range in range(width * resolution):
        #     self.offset_points[line_range] = curve.offset(
        #         self.curve, line_range/resolution, normals)

        #     for i in range(len(self.offset_points[line_range])-1):
        #         self.surface.extend(segment.discrete_segment(
        #             self.offset_points[line_range][i], self.offset_points[line_range][i+1], pixel_perfect=False))

        # print(self.surface)
