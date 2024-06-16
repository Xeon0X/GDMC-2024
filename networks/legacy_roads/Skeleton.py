import numpy as np
import skan
from skimage.morphology import skeletonize
from skan.csr import skeleton_to_csgraph
from collections import Counter
from PIL import Image
import random

from gdpc import Editor


class Skeleton:
    def __init__(self):
        self.lines = []
        self.intersections = []
        self.centers = []
        self.graph = []
        self.coordinates = []

    def setSkeleton(self, data):
        binary_skeleton = skeletonize(data)

        graph, coordinates = skeleton_to_csgraph(binary_skeleton)
        self.graph = graph.tocoo()

        # List of lists. Inverted coordinates.
        coordinates = list(coordinates)
        print(coordinates)
        for i in range(len(coordinates)):
            coordinates[i] = list(coordinates[i])

        print(coordinates)
        coordinates_final = []

        for i in range(len(coordinates[0])):
            print((coordinates[0][i], coordinates[1][i], coordinates[2][i]))
            coordinates_final.append(
                (coordinates[0][i], coordinates[1][i], coordinates[2][i]))

        self.coordinates = coordinates_final

    def findNextElements(self, key):
        """Find the very nearest elements"""

        line = []

        values = np.array(self.graph.row)
        indices = np.where(values == key)[0]

        for i in range(len(indices)):
            if self.graph.row[indices[i]] == key:
                line.append(self.graph.col[indices[i]])
        return line

    def findLine(self, key):
        nextKeys = self.findNextElements(key)

        if len(nextKeys) >= 3:  # Intersections.
            return nextKeys

        if len(nextKeys) == 2 or len(nextKeys) == 1:  # In line or endpoints.
            line = []
            line.append(key)
            line.insert(0, nextKeys[0])
            if len(nextKeys) == 2:
                line.insert(len(line), nextKeys[1])

            nextKeys = line[0], line[-1]

            while len(nextKeys) == 2 or len(nextKeys) == 1:
                extremity = []
                for key in nextKeys:
                    nextKeys = self.findNextElements(key)

                    if len(nextKeys) <= 2:
                        # Add the neighbors that is not already in the line.
                        for element in nextKeys:
                            if element not in line:
                                extremity.append(element)
                                line.append(element)

                    if len(nextKeys) >= 3:
                        # Add the intersection only.
                        extremity.append(key)

                    nextKeys = []
                    for key in extremity:
                        ends = self.findNextElements(key)
                        if len(ends) == 2:
                            nextKeys.append(key)
            return line

    def parseGraph(self):
        for key, value in sorted(
            Counter(self.graph.row).items(), key=lambda kv: kv[1], reverse=True
        ):
            # Start from the biggest intersections.
            if value != 2:  # We don't want to be in the middle of a line.
                line = self.findLine(key)

                # We have now all the connected points if it's an
                # intersection. We need to find the line.

                if value != 1:
                    # It's not an endpoint.
                    self.centers.append(key)
                    self.intersections.append(line)
                    for i in line:
                        line = self.findLine(i)

                        if i in line:
                            # The key is inside the result : it's a line.
                            alreadyInside = False
                            for l in self.lines:
                                # Verification if not already inside.
                                if Counter(l) == Counter(line):
                                    alreadyInside = True
                                    # print(line, "inside", lines)

                            if alreadyInside == False:
                                self.lines.append(line)
                        else:
                            # The key is not inside the result, it's an
                            # intersection directly connected to the key.
                            line = [key, i]
                            alreadyInside = False
                            for l in self.lines:
                                # Verification if not already inside.
                                if Counter(l) == Counter(line):
                                    alreadyInside = True
                                    # print(line, "inside", lines)

                            if alreadyInside == False:
                                self.lines.append(line)

    def map(self):
        """

        Generate an image to visualize 2D path of the skeleton.

        Returns:
            image: 2D path of the skeleton on top of the heightmap.
        """
        editor = Editor()

        buildArea = editor.getBuildArea()
        buildRect = buildArea.toRect()
        xzStart = buildRect.begin
        xzDistance = (max(buildRect.end[0], buildRect.begin[0]) - min(buildRect.end[0], buildRect.begin[0]), max(
            buildRect.end[1], buildRect.begin[1]) - min(buildRect.end[1], buildRect.begin[1]))

        heightmap = Image.open("data/heightmap.png").convert('RGB')
        roadsArea = Image.new("L", xzDistance, 0)
        width, height = heightmap.size

        # Lines
        for i in range(len(self.lines)):
            r, g, b = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))

            for j in range(len(self.lines[i])):

                z = self.coordinates[self.lines[i][j]][0]
                y = self.coordinates[self.lines[i][j]][1]
                x = self.coordinates[self.lines[i][j]][2]

                heightmap.putpixel(
                    (
                        int(z),
                        int(x),
                    ),
                    (r + j, g + j, b + j),
                )

                roadsArea.putpixel(
                    (
                        int(z),
                        int(x),
                    ),
                    (255),
                )

        # Centers
        for i in range(len(self.centers)):
            print(self.coordinates[self.centers[i]])
            heightmap.putpixel(
                (int(self.coordinates[self.centers[i]][0]), int(
                    self.coordinates[self.centers[i]][2])),
                (255, 255, 0),
            )

            roadsArea.putpixel(
                (int(self.coordinates[self.centers[i]][0]), int(
                    self.coordinates[self.centers[i]][2])),
                (255),
            )

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

        return heightmap, roadsArea
