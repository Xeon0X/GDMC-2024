import random
from collections import Counter
from typing import List, Union

import numpy as np
from gdpc import Editor
from PIL import Image, ImageDraw
from skan.csr import skeleton_to_csgraph
from skimage.morphology import skeletonize
from networks.geometry.Point3D import Point3D


def handle_import_image(image: Union[str, Image]) -> Image:
    if isinstance(image, str):
        return Image.open(image)
    return image


def simplify_coordinates(coordinates, epsilon):
    if len(coordinates) < 3:
        return coordinates

    # Find the point with the maximum distance
    max_distance = 0
    max_index = 0
    end_index = len(coordinates) - 1

    for i in range(1, end_index):
        distance = Point3D(coordinates[i][0], coordinates[i][1], coordinates[i][2]).distance(
            Point3D(coordinates[0][0], coordinates[0][1], coordinates[0][2]))
        if distance > max_distance:
            max_distance = distance
            max_index = i

    simplified_coordinates = []

    # If the maximum distance is greater than epsilon, recursively simplify
    if max_distance > epsilon:
        rec_results1 = simplify_coordinates(coordinates[:max_index+1], epsilon)
        rec_results2 = simplify_coordinates(coordinates[max_index:], epsilon)

        # Combine the simplified sub-results
        simplified_coordinates.extend(rec_results1[:-1])
        simplified_coordinates.extend(rec_results2)
    else:
        # The maximum distance is less than epsilon, retain the endpoints
        simplified_coordinates.append(coordinates[0])
        simplified_coordinates.append(coordinates[end_index])

    return simplified_coordinates


class Skeleton:
    def __init__(self, data: np.ndarray = None):
        self.lines = []
        self.intersections = []
        self.centers = []
        self.coordinates = []
        self.graph = None
        if data is not None:
            self.set_skeleton(data)

    def set_skeleton(self, data: np.ndarray):
        print("[Skeleton] Start skeletonization...")
        binary_skeleton = skeletonize(data, method="lee")

        graph, coordinates = skeleton_to_csgraph(binary_skeleton)
        self.graph = graph.tocoo()

        # List of lists. Inverted coordinates.
        coordinates = list(coordinates)
        # print(coordinates)
        for i in range(len(coordinates)):
            coordinates[i] = list(coordinates[i])
        # print(coordinates)

        for i in range(len(coordinates[0])):
            # print((coordinates[0][i], coordinates[1][i], coordinates[2][i]))
            self.coordinates.append(
                (coordinates[0][i], coordinates[1][i], coordinates[2][i]))
        print("[Skeleton] Skeletonization completed.")

    def find_next_elements(self, key: str) -> list:
        """Find the very nearest elements"""

        line = []

        values = np.array(self.graph.row)
        indices = np.where(values == key)[0]

        for i in range(len(indices)):
            if self.graph.row[indices[i]] == key:
                line.append(self.graph.col[indices[i]])
        return line

    def find_line(self, key: str):
        next_keys = self.find_next_elements(key)

        if len(next_keys) >= 3:  # Intersections.
            return next_keys

        if len(next_keys) == 2 or len(next_keys) == 1:  # In line or endpoints.
            line = [key]
            line.insert(0, next_keys[0])
            if len(next_keys) == 2:
                line.insert(len(line), next_keys[1])

            next_keys = line[0], line[-1]

            while len(next_keys) == 2 or len(next_keys) == 1:
                extremity = []
                for key in next_keys:
                    next_keys = self.find_next_elements(key)

                    if len(next_keys) <= 2:
                        # Add the neighbors that is not already in the line.
                        for element in next_keys:
                            if element not in line:
                                extremity.append(element)
                                line.append(element)

                    if len(next_keys) >= 3:
                        # Add the intersection only.
                        extremity.append(key)

                    next_keys = []
                    for key in extremity:
                        ends = self.find_next_elements(key)
                        if len(ends) == 2:
                            next_keys.append(key)
            return line

    def parse_graph(self, parse_orphan: bool = False):
        print("[Skeleton] Start parsing the graph",
              ("with orphans" if parse_orphan else "") + "...")
        for key, value in sorted(
                Counter(self.graph.row).items(), key=lambda kv: kv[1], reverse=True
        ):
            # Start from the biggest intersections.
            if value != 2:  # We don't want to be in the middle of a line.
                line = self.find_line(key)

                # We have now all the connected points if it's an
                # intersection. We need to find the line.

                if value != 1:
                    # It's not an endpoint.
                    self.centers.append(key)
                    self.intersections.append(line)
                    for i in line:
                        line = self.find_line(i)

                        if i in line:
                            # The key is inside the result : it's a line.
                            already_inside = False
                            for l in self.lines:
                                # Verification if not already inside.
                                if Counter(l) == Counter(line):
                                    already_inside = True
                                    # print(line, "inside", lines)

                            if not already_inside:
                                self.lines.append(line)
                        else:
                            # The key is not inside the result, it's an
                            # intersection directly connected to the key.
                            line = [key, i]
                            already_inside = False
                            for l in self.lines:
                                # Verification if not already inside.
                                if Counter(l) == Counter(line):
                                    already_inside = True
                                    # print(line, "inside", lines)

                            if not already_inside:
                                self.lines.append(line)
            elif value == 2 and parse_orphan:
                line = self.find_line(key)
                already_inside = False
                for l in self.lines:
                    # Verification if not already inside.
                    if Counter(l) == Counter(line):
                        already_inside = True

                if not already_inside:
                    self.lines.append(line)
        print("[Skeleton] Graph parsing completed.")

    def map(self) -> Image:
        """

        Generate an image to visualize 2D path of the skeleton.

        Returns:
            image: 2D path of the skeleton on top of the heightmap.
        """
        print("[Skeleton] Start mapping the skeleton...")
        # editor = Editor()

        # buildArea = editor.getBuildArea()
        # buildRect = buildArea.toRect()
        # xzStart = buildRect.begin
        # xzDistance = (max(buildRect.end[0], buildRect.begin[0]) - min(buildRect.end[0], buildRect.begin[0]),
        #              max(buildRect.end[1], buildRect.begin[1]) - min(buildRect.end[1], buildRect.begin[1]))

        heightmap = Image.open(
            "./world_maker/data/heightmap.png").convert('RGB')
        # roadsArea = Image.new("L", xzDistance, 0)
        # width, height = heightmap.size

        # Lines
        for i in range(len(self.lines)):
            r, g, b = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))

            for j in range(len(self.lines[i])):
                z = self.coordinates[self.lines[i][j]][0]
                # y = self.coordinates[self.lines[i][j]][1]
                x = self.coordinates[self.lines[i][j]][2]

                heightmap.putpixel(
                    (
                        int(z),
                        int(x),
                    ),
                    (r + j, g + j, b + j),
                )

                # roadsArea.putpixel(
                #    (
                #        int(z),
                #        int(x),
                #    ),
                #    (255),
                # )

        # Centers
        for i in range(len(self.centers)):
            # print(self.coordinates[self.centers[i]])
            heightmap.putpixel(
                (int(self.coordinates[self.centers[i]][0]), int(
                    self.coordinates[self.centers[i]][2])),
                (255, 255, 0),
            )

            # roadsArea.putpixel(
            #    (int(self.coordinates[self.centers[i]][0]), int(self.coordinates[self.centers[i]][2])),
            #    (255),
            # )

        # # Intersections
        # for i in range(len(self.intersections)):
        #     intersection = []
        #     for j in range(len(self.intersections[i])):
        #         intersection.append(self.coordinates[self.intersections[i][j]])

        #     for i in range(len(intersection)):
        #         heightmap.putpixel(
        #             (int(self.intersections[i][2]), int(self.intersections[i][0])),
        #             (255, 0, 255),
        #         )
        print("[Skeleton] Mapping completed.")
        return heightmap  # , roadsArea

    def road_area(self, name: str, radius: int = 10) -> Image:
        print("[Skeleton] Start mapping the road area...")
        heightmap = Image.open("./world_maker/data/heightmap.png")
        width, height = heightmap.size
        road_area_map = Image.new("L", (width, height), 0)
        road_area_map_draw = ImageDraw.Draw(road_area_map)

        # Lines
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])):
                z = self.coordinates[self.lines[i][j]][0]
                x = self.coordinates[self.lines[i][j]][2]
                circle_coords = (z - radius, x - radius,
                                 z + radius, x + radius)
                road_area_map_draw.ellipse(circle_coords, fill=255)

        # Centers
        for i in range(len(self.centers)):
            z = self.coordinates[self.centers[i]][0]
            x = self.coordinates[self.centers[i]][2]
            circle_coords = (z - radius, x - radius, z + radius, x + radius)
            road_area_map_draw.ellipse(circle_coords, fill=255)

        road_area_map.save("./world_maker/data/"+name)

        print("[Skeleton] Road area mapping completed.")
        return road_area_map
