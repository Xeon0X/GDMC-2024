from gdpc import Block as place
from gdpc import Editor
import networks.legacy_roads.maths as maths


USE_BATCHING = True
editor = Editor(buffering=True, caching=True, multithreading=True)


def setBlock(block, xyz):
    x, y, z = xyz
    editor.placeBlock((x, y, z), place(block))


def getBlock(xyz):
    print("You used getBlock in a deprecated manner.")
    # x, y, z = xyz
    # return minecraft.getBlock(x, y, z)


def fillBlock(block, xyz):
    print("fill", xyz)
    xDistance = max(xyz[0], xyz[3]) - min(xyz[0], xyz[3])
    yDistance = max(xyz[1], xyz[4]) - min(xyz[1], xyz[4])
    zDistance = max(xyz[2], xyz[5]) - min(xyz[2], xyz[5])

    coordinates = []

    for i in range(min(xyz[0], xyz[3]), max(xyz[0], xyz[3])+1):
        for j in range(min(xyz[1], xyz[4]), max(xyz[1], xyz[4])+1):
            for k in range(min(xyz[2], xyz[5]), max(xyz[2], xyz[5])+1):
                coordinates.append((i, j, k))

    editor.placeBlock(coordinates, place(block))


def setLine(block, xyz0, xyz1, pixelPerfect=True):
    points = maths.line(xyz0, xyz1, pixelPerfect)
    for i in points:
        setBlock(block, (i[0], i[1], i[2]))
