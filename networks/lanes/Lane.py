import networks.geometry.curve as curve
import networks.geometry.CurveSurface as CurveSurface
import networks.geometry.segment as segment
import random


class Lane:
    def __init__(self, coordinates, lane_materials,  width):
        self.coordinates = coordinates
        self.width = width
        self.lane_materials = lane_materials
        self.surface = []

    def get_surface(self):
        resolution, distance = curve.resolution_distance(self.coordinates, 6)

        curve_points = curve.curve(self.coordinates, resolution)
        curve_surface = CurveSurface.CurveSurface(self.coordinates)
        curve_surface.compute_curvature()

        # Set the road to be flat
        normals = []
        for i in range(len(curve_surface.curvature)):
            normals.append((0, 1, 0))

        # Compute each line
        for distance in range(self.width):
            offset = curve.offset(curve_surface.curve, distance, normals)
            for i in range(len(offset)-1):
                line = segment.discrete_segment(offset[i], offset[i+1])
                for coordinate in line:
                    self.surface.append((coordinate, random.choices(
                        list(self.lane_materials.keys()),
                        weights=self.lane_materials.values(),
                        k=1,)))

        return self.surface
