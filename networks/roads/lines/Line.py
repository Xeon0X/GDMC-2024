import networks.geometry.curve_tools as curve_tools
import networks.geometry.segment_tools as segment_tools
import random


class Line:
    def __init__(self, coordinates, line_materials):
        self.coordinates = coordinates
        self.line_materials = line_materials
        self.surface = []

    def get_surface(self):
        resolution, distance = curve_tools.resolution_distance(
            self.coordinates, 6)

        curve_points = curve_tools.curve(self.coordinates, resolution)

        # Compute the line

        pattern_length = 0
        pattern_materials = []

        for pattern in self.line_materials:
            pattern_length += pattern[1]
            for _ in range(pattern[1]):
                pattern_materials.append(pattern[0])

        pattern_iteration = 0
        for i in range(len(curve_points)-1):
            line = segment_tools.discrete_segment(
                curve_points[i], curve_points[i+1])
            for coordinate in line:
                block = random.choices(
                    list(pattern_materials[pattern_iteration].keys()),
                    weights=pattern_materials[pattern_iteration].values(),
                    k=1)[0]
                if block != 'None':
                    self.surface.append((coordinate, block))

                pattern_iteration += 1
                if pattern_iteration >= pattern_length:
                    pattern_iteration = 0

        return self.surface
