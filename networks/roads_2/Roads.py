import json
from typing import List
from networks.geometry.Polyline import Polyline

from networks.geometry.Point3D import Point3D
from networks.geometry.Point2D import Point2D
from networks.geometry.Circle import Circle
from Enums import LINE_THICKNESS_MODE
from gdpc import Block, Editor


class Road:
    def __init__(self, coordinates: List[Point3D], width: int):
        self.coordinates = coordinates
        self.output_block = []
        # with open(road_configuration) as f:
        #     self.road_configuration = json.load(f)
        #     self.width = self.road_configuration["width"]
        self.width = width
        self.polyline_height = None

        self.polyline = Polyline(Point3D.to_2d(coordinates, 'y'))
        self.polyline_total_line_output = [
            [] for _ in range(len(self.polyline.total_line_output))]
        self.index_factor = 0

        self._projection()
        self._surface()

    def _surface(self):
        # Segments

        for i in range(1, len(self.polyline.segments)):
            if len(self.polyline.segments[i].segment()) > 1:
                for j in range(len(self.polyline.segments[i].segment_thick(self.width, LINE_THICKNESS_MODE.MIDDLE))):
                    # Get nearest in x,z projection
                    nearest = self.polyline.segments[i].points_thick[j].nearest(
                        Point3D.to_2d(self.polyline_total_line_output, removed_axis='y'), True)
                    self.output_block.append(
                        (Point3D.insert_3d([self.polyline.segments[i].points_thick[j]], 'y', [self.polyline_total_line_output[nearest[0]].y])[0].coordinates, Block("stone")))

        for i in range(1, len(self.polyline.centers)-1):
            # Circle

            circle = Circle(self.polyline.centers[i])
            circle.circle_thick(int(
                (self.polyline.radii[i]-self.width/2)), int((self.polyline.radii[i]+self.width/2)-1))

            # Better to do here than drawing circle arc inside big triangle!
            double_point_a = Point2D.from_arrays(Point2D.to_arrays(self.polyline.acrs_intersections[i][0]) + 5 * (Point2D.to_arrays(
                self.polyline.acrs_intersections[i][0]) - Point2D.to_arrays(self.polyline.centers[i])))
            double_point_b = Point2D.from_arrays(Point2D.to_arrays(self.polyline.acrs_intersections[i][2]) + 5 * (Point2D.to_arrays(
                self.polyline.acrs_intersections[i][2]) - Point2D.to_arrays(self.polyline.centers[i])))

            for j in range(len(circle.points_thick)):
                if circle.points_thick[j].is_in_triangle(double_point_a, self.polyline.centers[i], double_point_b):
                    nearest = circle.points_thick[j].nearest(
                        Point3D.to_2d(self.polyline_total_line_output, removed_axis='y'), True)
                    self.output_block.append(
                        (Point3D.insert_3d([circle.points_thick[j]], 'y', [
                            self.polyline_total_line_output[nearest[0]].y])[0].coordinates, Block("white_concrete")))

    def _projection(self):
        nearest_points_to_reference = []
        for i in range(len(self.coordinates)):
            # nearest_points_to_reference.append(Point3D.insert_3d([Point3D.to_2d([self.coordinates[i]], 'y')[0].nearest(
            #     self.polyline.total_line_output, return_index=True)], 'y', [self.coordinates[i].y])[0])
            index, point = Point3D.to_2d([self.coordinates[i]], 'y')[0].nearest(
                self.polyline.total_line_output, return_index=True)
            nearest_points_to_reference.append(
                Point2D(index, self.coordinates[i].y))

        self.polyline_height = Polyline(nearest_points_to_reference)

        self.index_factor = len(
            self.polyline_height.total_line_output)/len(self.polyline.total_line_output)

        for i in range(len(self.polyline.total_line_output)):
            self.polyline_total_line_output[i] = Point3D(
                self.polyline.total_line_output[i].x, self.polyline_height.total_line_output[round(i*self.index_factor)].y, self.polyline.total_line_output[i].y)

        self.polyline_total_line_output = self.polyline_total_line_output[0].optimized_path(
            self.polyline_total_line_output)

    def place(self):
        editor = Editor(buffering=True)
        for i in range(len(self.output_block)):
            editor.placeBlock(self.output_block[i][0],
                              self.output_block[i][1])
