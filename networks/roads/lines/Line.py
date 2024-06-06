import networks.geometry.curve_tools as curve_tools
import networks.geometry.segment_tools as segment_tools
import random


class Line:
    def __init__(self, coordinates, line_materials):
        self.coordinates = coordinates  # Full lines coordinates, not just endpoints
        self.line_materials = line_materials  # From lines.json
        self.coordinates_with_blocks = []  # Output

    def get_blocks(self):
        pattern_length = 0
        pattern_materials = []

        # Create the pattern materials list with correct materials depending on the selected pattern.
        for pattern in self.line_materials:
            pattern_length += pattern[1]
            for _ in range(pattern[1]):
                pattern_materials.append(pattern[0])

        pattern_iteration = 0
        for coordinate in self.coordinates:
            block = random.choices(
                list(pattern_materials[pattern_iteration].keys()),
                weights=pattern_materials[pattern_iteration].values(),
                k=1)[0]
            if block != 'None':
                self.coordinates_with_blocks.append((coordinate, block))

            pattern_iteration += 1
            if pattern_iteration >= pattern_length:
                pattern_iteration = 0

        return self.coordinates_with_blocks
