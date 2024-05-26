import networks.geometry.curve as curve
import networks.geometry.segment as segment
import random


class Line:
    def __init__(self, coordinates, line_type):
        self.coordinates = coordinates
        self.line_type = line_type
        self.surface = []

    def get_surface(self):
        resolution, distance = curve.resolution_distance(self.coordinates, 6)

        curve_points = curve.curve(self.coordinates, resolution)

        # Compute the line

        pattern_length = 0
        pattern_materials = []
        for key, value in self.line_type.items():
            pattern_length += int(key)
            for _ in range(int(key)):
                pattern_materials.append(value)

        pattern_iteration = 0
        for i in range(len(curve_points)-1):
            line = segment.discrete_segment(curve_points[i], curve_points[i+1])
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
