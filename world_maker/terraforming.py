from typing import Union

import numpy as np
from gdpc import Editor, Block, geometry, lookup
from PIL import Image
from skimage import morphology

from world_maker.data_analysis import handle_import_image


def remove_trees(heightmap: Union[str, Image], treesmap: Union[str, Image], mask: Union[str, Image]):
    print("[Remove tree] Starting...")
    editor = Editor(buffering=True)
    build_area = editor.getBuildArea()
    build_rectangle = build_area.toRect()

    start = build_rectangle.begin

    distance = (max(build_rectangle.end[0], build_rectangle.begin[0]) - min(build_rectangle.end[0], build_rectangle.begin[0]), max(
        build_rectangle.end[1], build_rectangle.begin[1]) - min(build_rectangle.end[1], build_rectangle.begin[1]))

    heightmap = handle_import_image(heightmap).convert('L')
    treesmap = handle_import_image(treesmap).convert('L')
    mask = handle_import_image(mask)

    removed_treesmap = Image.new("L", distance, 0)

    removed = []
    for x in range(0, distance[0]):
        for z in range(0, distance[1]):

            if mask.getpixel((x, z)) != 0 and treesmap.getpixel((x, z)) > 0 and (x, z) not in removed:

                tree_area = morphology.flood(treesmap, (z, x), tolerance=1)
                blend = Image.blend(Image.fromarray(tree_area).convert(
                    'L'), removed_treesmap.convert('L'), 0.5)

                array = np.array(blend.convert('L'))
                bool_array = array > 1
                removed_treesmap = Image.fromarray(bool_array)

                removed.append((x, z))

    for x in range(0, distance[0]):
        for z in range(0, distance[1]):
            if removed_treesmap.getpixel((x, z)) != 0:
                y = heightmap.getpixel((x, z))
                y_top = removed_treesmap.getpixel((x, z))
                geometry.placeLine(
                    editor, (start[0] + x, y+1, start[1] + z), (start[0] + x, y_top, start[1] + z), Block('air'))

    removed_treesmap.save('./world_maker/data/removed_treesmap.png')
    print("[Remove tree] Done.")


def smooth_terrain(heightmap: Union[str, Image], heightmap_smooth: Union[str, Image], mask: Union[str, Image]):

    print("[Smooth terrain] Starting...")
    editor = Editor(buffering=True)
    build_area = editor.getBuildArea()
    build_rectangle = build_area.toRect()

    start = build_rectangle.begin

    distance = (max(build_rectangle.end[0], build_rectangle.begin[0]) - min(build_rectangle.end[0], build_rectangle.begin[0]), max(
        build_rectangle.end[1], build_rectangle.begin[1]) - min(build_rectangle.end[1], build_rectangle.begin[1]))

    heightmap = handle_import_image(heightmap).convert('L')
    heightmap_smooth = handle_import_image(heightmap_smooth).convert('L')
    mask = handle_import_image(mask).convert('L')

    smooth_terrain_delta = Image.new("RGB", distance, 0)

    slice = editor.loadWorldSlice(build_rectangle)
    smoothable_blocks = lookup.OVERWORLD_SOILS | lookup.OVERWORLD_STONES | lookup.SNOWS

    for x in range(0, distance[0]):
        for z in range(0, distance[1]):

            if mask.getpixel((x, z)) != 0:
                y = heightmap.getpixel((x, z))
                y_smooth = heightmap_smooth.getpixel((x, z))
                delta = y - y_smooth
                smooth_terrain_delta.putpixel((x, z), delta)

                if delta != 0:
                    block = slice.getBlock((x, y, z))
                    if block.id in smoothable_blocks:
                        if delta > 0:
                            geometry.placeLine(
                                editor, (start[0] + x, y, start[1] + z), (start[0] + x, y_smooth, start[1] + z), Block('air'))
                            editor.placeBlock(
                                (start[0] + x, y_smooth, start[1] + z), block)

                        else:
                            geometry.placeLine(
                                editor, (start[0] + x, y, start[1] + z), (start[0] + x, y_smooth, start[1] + z), block)

    smooth_terrain_delta.save('./world_maker/data/smooth_terrain_delta.png')
    print("[Smooth terrain] Done.")
