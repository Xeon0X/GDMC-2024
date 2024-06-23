import json
from typing import List
from networks.geometry.Polyline import Polyline

from networks.geometry.Point3D import Point3D
from networks.geometry.Point2D import Point2D
from networks.geometry.Segment2D import Segment2D
from networks.geometry.Segment3D import Segment3D
from networks.geometry.Circle import Circle
from utils.Enums import LINE_THICKNESS_MODE
from gdpc import Block, Editor, geometry
from scipy.ndimage import gaussian_filter1d
import numpy as np


class Road:
    def __init__(self, coordinates: List[Point3D], width: int):
        self.coordinates = self._remove_collinear_points(coordinates)
        self.output_block = []
        # with open(road_configuration) as f:
        #     self.road_configuration = json.load(f)
        #     self.width = self.road_configuration["width"]
        self.width = width
        self.polyline_height = None
        self.polyline_total_line_output = None
        self.segment_total_line_output = None
        self.index_factor = 0

        if len(self._remove_collinear_points(self.coordinates)) >= 4:
            self.polyline = Polyline(Point3D.to_2d(coordinates, 'y'))
            self.polyline_total_line_output = [
                [] for _ in range(len(self.polyline.total_line_output))]

            self._projection_polyline()

        if len(self.coordinates) == 2:
            self.segment_total_line_output = Segment2D(
                Point3D.to_2d([self.coordinates[0]], 'y')[0], Point3D.to_2d([self.coordinates[1]], 'y')[0]).segment_thick(self.width, LINE_THICKNESS_MODE.MIDDLE)
            self._projection_segment()
            self.place()

    @staticmethod
    def _remove_collinear_points(points):
        output_points = [points[0]]

        for i in range(1, len(points) - 1):
            if isinstance(points[0], Point3D):
                if not Point2D.collinear(
                        Point3D.to_2d([points[i-1]], 'y')[0], Point3D.to_2d([points[i]], 'y')[0], Point3D.to_2d([points[i+1]], 'y')[0]):
                    output_points.append(points[i])
            else:
                if not Point2D.collinear(points[i-1], points[i], points[i+1]):
                    output_points.append(points[i])

        output_points.append(points[-1])
        return output_points

    def _surface(self):
        for i in range(1, len(self.polyline.segments)):
            # Segments
            if len(self.polyline.segments[i].segment()) > 2:
                last_valid_index = i
                self.polyline.segments[i].segment_thick(
                    self.width, LINE_THICKNESS_MODE.MIDDLE)
                for k in range(len(self.polyline.segments[i].points_thick_by_line)):
                    kk = k % 7
                    match kk:
                        case 0:
                            blob = 'pink_concrete'
                        case 1:
                            blob = 'red_concrete'
                        case 2:
                            blob = 'orange_concrete'
                        case 3:
                            blob = 'yellow_concrete'
                        case 4:
                            blob = 'green_concrete'
                        case 5:
                            blob = 'blue_concrete'
                        case 6:
                            blob = 'purple_concrete'

                    for m in range(len(self.polyline.segments[i].points_thick_by_line[k])):
                        nearest = self.polyline.segments[i].points_thick_by_line[k][m].nearest(
                            Point3D.to_2d(self.polyline_total_line_output, removed_axis='y'), True)
                        self.output_block.append(
                            (Point3D.insert_3d([self.polyline.segments[i].points_thick_by_line[k][m]], 'y', [self.polyline_total_line_output[nearest[0]].y])[0].coordinates, Block(blob)))

                    for m in range(len(self.polyline.segments[i].gaps[k])):
                        nearest = self.polyline.segments[i].gaps[k][m].nearest(
                            Point3D.to_2d(self.polyline_total_line_output, removed_axis='y'), True)
                        self.output_block.append(
                            (Point3D.insert_3d([self.polyline.segments[i].gaps[k][m]], 'y', [self.polyline_total_line_output[nearest[0]].y])[0].coordinates, Block("black_concrete")))

            # Circle
            if i != len(self.polyline.segments)-1:
                circle, gaps = Circle(self.polyline.centers[i]).circle_thick_by_line(int(
                    (self.polyline.radii[i]-self.width/2))+1, int((self.polyline.radii[i]+self.width/2))+1)

                # Better to do here than drawing circle arc inside big triangle!
                double_point_a = Point2D.from_arrays(Point2D.to_arrays(self.polyline.acrs_intersections[i][0]) + 50 * (Point2D.to_arrays(
                    self.polyline.acrs_intersections[i][0]) - Point2D.to_arrays(self.polyline.centers[i])))
                double_point_b = Point2D.from_arrays(Point2D.to_arrays(self.polyline.acrs_intersections[i][2]) + 50 * (Point2D.to_arrays(
                    self.polyline.acrs_intersections[i][2]) - Point2D.to_arrays(self.polyline.centers[i])))

                circle_list = [[] for _ in range(len(circle))]
                for j in range(len(circle)):
                    for k in range(len(circle[j])):
                        if circle[j][k].is_in_triangle(double_point_a, self.polyline.centers[i], double_point_b):
                            circle_list[j].append(circle[j][k])

                # for j in range(len(gaps)):
                #     for k in range(len(gaps[j])):
                #         if gaps[j][k].is_in_triangle(double_point_a, self.polyline.centers[i], double_point_b):
                #             circle_list[j].append(gaps[j][k])

                middle_lane_index = round(len(circle_list)/2)
                middle_line_length = len(circle_list[middle_lane_index])
                circle_list[middle_lane_index] = circle_list[middle_lane_index][-1].optimized_path(
                    circle_list[middle_lane_index])
                for k in range(len(circle_list[middle_lane_index])):
                    nearest = circle_list[middle_lane_index][k].nearest(
                        Point3D.to_2d(self.polyline_total_line_output, removed_axis='y'), True)
                    circle_list[middle_lane_index][k] = Point3D.insert_3d([circle_list[middle_lane_index][k]], 'y', [
                        self.polyline_total_line_output[nearest[0]].y])[0]

                for j in range(len(circle_list)):
                    if j != middle_lane_index:
                        circle_list[j] = circle_list[j][0].optimized_path(
                            circle_list[j])
                        factor = (middle_line_length-1)/(len(circle_list[j])-1)

                        for k in range(len(circle_list[j])):
                            circle_list[j][k] = Point3D.insert_3d([circle_list[j][k]], 'y', [
                                circle_list[middle_lane_index][round(factor * k)].y])[0]

                    # Complete with gaps
                    if j < len(gaps):
                        for k in range(len(gaps[j])):
                            if gaps[j][k].is_in_triangle(double_point_a, self.polyline.centers[i], double_point_b):
                                circle_list[j].append(
                                    Point3D.insert_3d([gaps[j][k]], 'y', [
                                        circle_list[j][gaps[j][k].nearest(Point3D.to_2d(circle_list[j], 'y'), True)[0]].y])[0])

                    kk = j % 7
                    match kk:
                        case 0:
                            blob = 'pink_concrete'
                        case 1:
                            blob = 'red_concrete'
                        case 2:
                            blob = 'orange_concrete'
                        case 3:
                            blob = 'yellow_concrete'
                        case 4:
                            blob = 'green_concrete'
                        case 5:
                            blob = 'blue_concrete'
                        case 6:
                            blob = 'purple_concrete'
                    for k in range(len(circle_list[j])):
                        self.output_block.append(
                            (circle_list[j][k].coordinates, Block(blob)))

    def _projection_gaussian(self):
        nearest_points_to_reference = []
        for i in range(len(self.coordinates)):
            # Index is used to space accordingly
            index, point = Point3D.to_2d([self.coordinates[i]], 'y')[0].nearest(
                self.polyline.total_line_output, return_index=True)
            nearest_points_to_reference.append(
                Point2D(index, self.coordinates[i].y))

        linear_y_interpolation = []
        for i in range(len(nearest_points_to_reference)-1):
            linear_y_interpolation.extend(Segment2D(
                nearest_points_to_reference[i], nearest_points_to_reference[i+1]).segment())

        linear_y_interpolation = np.array(
            Point2D.to_arrays(linear_y_interpolation))

        # Extract x and y coordinates
        x = linear_y_interpolation[:, 0]
        y = linear_y_interpolation[:, 1]

        y_smooth = gaussian_filter1d(y, sigma=5)

        self.index_factor = len(y_smooth)/len(self.polyline.total_line_output)

        for i in range(len(self.polyline.total_line_output)):
            self.polyline_total_line_output[i] = Point3D(
                self.polyline.total_line_output[i].x, y[round(i*self.index_factor)], self.polyline.total_line_output[i].y)

        self._surface()
        self.place()

    def _projection_polyline(self):
        nearest_points_to_reference = []
        for i in range(len(self.coordinates)):
            # nearest_points_to_reference.append(Point3D.insert_3d([Point3D.to_2d([self.coordinates[i]], 'y')[0].nearest(
            #     self.polyline.total_line_output, return_index=True)], 'y', [self.coordinates[i].y])[0])
            index, point = Point3D.to_2d([self.coordinates[i]], 'y')[0].nearest(
                self.polyline.total_line_output, return_index=True)
            nearest_points_to_reference.append(
                Point2D(index, self.coordinates[i].y))

        if len(self._remove_collinear_points(nearest_points_to_reference)) >= 4:
            self.polyline_height = Polyline(nearest_points_to_reference)

            self.index_factor = len(
                self.polyline_height.total_line_output)/len(self.polyline.total_line_output)

            for i in range(len(self.polyline.total_line_output)):
                self.polyline_total_line_output[i] = Point3D(
                    self.polyline.total_line_output[i].x, self.polyline_height.total_line_output[round(i*self.index_factor)].y+70, self.polyline.total_line_output[i].y)

            self._surface()
            self.place()
        # self.polyline_total_line_output = self.polyline_total_line_output[0].optimized_path(
        #     self.polyline_total_line_output)

    def _projection_segment(self):
        s = Segment3D(
            self.coordinates[0], self.coordinates[1])

        reference = s.segment()

        for i in range(len(self.segment_total_line_output)):
            self.output_block.append(((
                self.segment_total_line_output[i].x, reference[self.segment_total_line_output[i].nearest(Point3D.to_2d(reference, 'y'), True)[0]].y, self.segment_total_line_output[i].y), Block("black_concrete")))

    def place(self):
        editor = Editor(buffering=True)
        for i in range(len(self.output_block)):
            editor.placeBlock(self.output_block[i][0],
                              self.output_block[i][1])
