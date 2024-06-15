from gdpc import Editor, geometry, lookup
import numpy as np
from PIL import Image
from world_maker.Block import Block

waterBiomes = [
    "minecraft:ocean",
    "minecraft:deep_ocean",
    "minecraft:warm_ocean",
    "minecraft:lukewarm_ocean",
    "minecraft:deep_lukewarm_ocean",
    "minecraft:cold_ocean",
    "minecraft:deep_cold_ocean",
    "minecraft:frozen_ocean",
    "minecraft:deep_frozen_ocean",
    "minecraft:mushroom_fieds",
    "minecraft:river",
    "minecraft:frozen_river",
]

waterBlocks = [
    "minecraft:water",
]


class World:
    def __init__(self):

        editor = Editor(buffering=True)
        buildArea = editor.getBuildArea()

        self.coordinates_min = [min(buildArea.begin[i], buildArea.last[i]) for i in range(3)]
        self.coordinates_max = [max(buildArea.begin[i], buildArea.last[i]) for i in range(3)]

        self.length_x = self.coordinates_max[0] - self.coordinates_min[0] + 1
        self.length_y = self.coordinates_max[1] - self.coordinates_min[1] + 1
        self.length_z = self.coordinates_max[2] - self.coordinates_min[2] + 1

        self.volume = [[[None for _ in range(self.length_z)] for _ in range(self.length_y)] for _ in
                       range(self.length_x)]

    def isInVolume(self, coordinates):
        if (self.coordinates_min[0] <= coordinates[0] <= self.coordinates_max[0] and
                self.coordinates_min[1] <= coordinates[1] <= self.coordinates_max[1] and
                self.coordinates_min[2] <= coordinates[2] <= self.coordinates_max[2]):
            return True
        return False

    def addBlocks(self, blocks: list[Block]):
        """
        Add block or list of block to the volume.
        """

        for block in blocks:
            if self.isInVolume(block.coordinates):
                self.volume[block.coordinates[0] - self.coordinates_min[0]][
                    block.coordinates[1] - self.coordinates_min[1]][
                    block.coordinates[2] - self.coordinates_min[2]] = block

    def removeBlock(self, volumeCoordinates):
        """
        Add block or list of block to the volume.
        """

        self.volume[volumeCoordinates[0]][volumeCoordinates[1]][volumeCoordinates[2]] = None

    def getBlockFromCoordinates(self, coordinates):
        """
        Use already created volume to get block data.
        """

        editor = Editor(buffering=True)
        if self.volume[coordinates[0] - self.coordinates_min[0]][coordinates[1] - self.coordinates_min[1]][
            coordinates[2] - self.coordinates_min[2]] == None:
            self.volume[coordinates[0] - self.coordinates_min[0]][coordinates[1] - self.coordinates_min[1]][
                coordinates[2] - self.coordinates_min[2]] = Block((coordinates[0], coordinates[1], coordinates[2]),
                                                                  editor.getBlock((coordinates[0], coordinates[1],
                                                                                   coordinates[2])).id)

        return self.volume[coordinates[0] - self.coordinates_min[0]][coordinates[1] - self.coordinates_min[1]][
            coordinates[2] - self.coordinates_min[2]]

    def getNeighbors(self, Block):
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if not (i == 0 and j == 0 and k == 0):
                        coordinates = (Block.coordinates[0] + i, Block.coordinates[1] + j, Block.coordinates[2] + k)
                        if self.isInVolume(coordinates):
                            Block.addNeighbors([self.getBlockFromCoordinates(coordinates)])

    def setVolume(self):
        """
        Scan the world with no optimization. Not tested on large areas.
        """

        editor = Editor(buffering=True)

        for x in range(self.coordinates_min[0], self.coordinates_max[0] + 1):
            for y in range(self.coordinates_min[1], self.coordinates_max[1] + 1):
                for z in range(self.coordinates_min[2], self.coordinates_max[2] + 1):
                    self.addBlocks([Block((x, y, z), editor.getBlock((x, y, z)).id)])

    def getData(self):
        """
        Generate all needed datas for the generator : heightmap, watermap, and preset the volume with data from the heightmap.
        """

        editor = Editor()
        buildArea = editor.getBuildArea()
        buildRect = buildArea.toRect()

        xzStart = buildRect.begin
        print("[World]", '('+str(xzStart[0])+', '+str(xzStart[1])+')',  "xzStart")
        xzDistance = (max(buildRect.end[0], buildRect.begin[0]) - min(buildRect.end[0], buildRect.begin[0]),
                      max(buildRect.end[1], buildRect.begin[1]) - min(buildRect.end[1], buildRect.begin[1]))
        watermap = Image.new("L", xzDistance, 0)
        heightmap = Image.new("RGBA", xzDistance, 0)
        treesmap = Image.new("RGBA", xzDistance, 0)

        slice = editor.loadWorldSlice(buildRect)

        heightmapData = list(np.array(slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"], dtype=np.uint8))
        treesmapData = list(np.array(slice.heightmaps["MOTION_BLOCKING"], dtype=np.uint8))

        for x in range(0, xzDistance[0]):
            for z in range(0, xzDistance[1]):
                y = heightmapData[x][z] - 1
                yTree = treesmapData[x][z] - 1

                biome = slice.getBiome((x, y, z))
                block = slice.getBlock((x, y, z))
                maybeATree = slice.getBlock((x, yTree, z))

                if maybeATree.id in lookup.TREES:
                    treesmap.putpixel((x, z), (yTree, yTree, yTree))

                if block.id not in lookup.TREES:
                    heightmap.putpixel((x, z), (y, y, y))
                else:
                    height = 0
                    number = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i != 0 or j != 0:
                                if (0 <= x + i < xzDistance[0]) and (0 <= z + j < xzDistance[1]):
                                    k = heightmapData[x + i][z + j] - 1

                                    # print('getData for tree', xzStart[0] + x + i, k, xzStart[1] + z + j)

                                    blockNeighbor = slice.getBlock((x + i, k, z + j))
                                    if blockNeighbor.id not in lookup.TREES:
                                        height += k
                                        number += 1
                    if number != 0:
                        average = round(height / number)
                        # print(average, "average")
                        heightmap.putpixel((x, z), (average, average, average))

                if (biome in waterBiomes) or (block.id in waterBlocks):
                    watermap.putpixel((x, z), 255)
                else:
                    watermap.putpixel((x, z), 0)

                self.addBlocks([Block((xzStart[0] + x, 100, xzStart[1] + z), block)])  # y set to 100 for 2D

        return heightmap, watermap, treesmap

    def propagate(self, coordinates, scanned=[]):
        i = 0
        editor = Editor(buffering=True)
        if self.isInVolume(coordinates):
            Block = self.getBlockFromCoordinates(coordinates)
            self.getNeighbors(Block)
            for neighbor in Block.neighbors:
                if neighbor not in scanned:
                    scanned.append(neighbor)
                    self.getNeighbors(neighbor)
                    if neighbor.isSurface():
                        self.propagate(neighbor.coordinates, scanned)

    def volumeTo3DBinaryImage(self):
        binaryImage = []
        for x in range(self.length_x):
            binaryImage.append([])
            for y in range(self.length_y):
                binaryImage[x].append([])
                for z in range(self.length_z):
                    if self.volume[x][y][z] != None:
                        binaryImage[x][y].append(True)
                    else:
                        binaryImage[x][y].append(False)

        return np.array(binaryImage)

    def maskVolume(self, mask):
        """

        Delete unusable area of the volume to not let it be use by the skeletonize, based on a filtered image that act as a mask.

        Args:
            mask (image): white or black image : combined watermap smoothed and sobel smoothed.
        """
        editor = Editor()
        buildArea = editor.getBuildArea()
        buildRect = buildArea.toRect()

        xzStart = buildRect.begin
        xzDistance = (max(buildRect.end[0], buildRect.begin[0]) - min(buildRect.end[0], buildRect.begin[0]),
                      max(buildRect.end[1], buildRect.begin[1]) - min(buildRect.end[1], buildRect.begin[1]))

        mask = Image.open(mask)

        slice = editor.loadWorldSlice(buildRect)

        heightmapData = list(np.array(slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"], dtype=np.uint8))

        for x in range(0, xzDistance[0]):
            for z in range(0, xzDistance[1]):
                y = heightmapData[x][z] - 1
                if mask.getpixel((x, z)) == 255:
                    self.removeBlock((x, 100, z))  # y set to 100 for 2D

    def simplifyVolume(self):
        array = self.volumeTo3DBinaryImage()
        # array = ndimage.binary_dilation(array, iterations=15)

        return array


if __name__ == "__main__":
    w = World()
    w.getData()