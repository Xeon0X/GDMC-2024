from typing import Union

import numpy as np
from gdpc import Editor, Block, geometry
from PIL import Image
from skimage import morphology

from world_maker.data_analysis import handle_import_image


def remove_trees(heightmap: Union[str, Image], treesmap: Union[str, Image], mask: Union[str, Image], ):

    editor = Editor(buffering=True)
    build_area = editor.getBuildArea()
    build_rectangle = build_area.toRect()

    start = build_rectangle.begin

    distance = (max(build_rectangle.end[0], build_rectangle.begin[0]) - min(build_rectangle.end[0], build_rectangle.begin[0]), max(
        build_rectangle.end[1], build_rectangle.begin[1]) - min(build_rectangle.end[1], build_rectangle.begin[1]))

    heightmap = handle_import_image(heightmap).convert('L')
    treesmap = handle_import_image(treesmap).convert('L')
    mask = handle_import_image(mask)

    removed_treesmap = Image.new("RGB", distance, 0)

    removed = []
    for x in range(0, distance[0]):
        for z in range(0, distance[1]):

            if mask.getpixel((x, z)) == 255 and treesmap.getpixel((x, z)) > 0 and (x, z) not in removed:

                treeArea = morphology.flood(treesmap, (z, x), tolerance=1)
                blend = Image.blend(Image.fromarray(treeArea).convert(
                    'RGB'), removed_treesmap.convert('RGB'), 0.5)

                array = np.array(blend.convert('L'))
                bool_array = array > 1
                removed_treesmap = Image.fromarray(bool_array)

                removed.append((x, z))
                print(x, z)

    removed_treesmap.save('./world_maker/data/removed_treesmap.png')

    for x in range(0, distance[0]):
        for z in range(0, distance[1]):
            print("removing tree in ", start[0] + x, start[1] + z)
            if removed_treesmap.getpixel((x, z)) != 0:
                y = heightmap.getpixel((x, z))
                y_top = removed_treesmap.getpixel((x, z))
                geometry.placeLine(
                    editor, (start[0] + x, y+1, start[1] + z), (start[0] + x, y_top, start[1] + z), Block('air'))
