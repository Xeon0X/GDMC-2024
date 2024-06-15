import random
from world_maker.world_maker import *
from House import *

def main():
    rectangle_house_mountain, rectangle_building, skeleton_highway, skeleton_mountain = world_maker()
    
    editor = Editor()
    blocks = {
        "wall": "blackstone",
        "roof": "blackstone",
        "roof_slab": "blackstone_slab",
        "door": "oak_door",
        "window": "glass_pane",
        "entrance": "oak_door",
        "stairs": "quartz_stairs",
        "stairs_slab": "quartz_slab",
        "celling": "quartz_block",
        "floor": "quartz_block",
        "celling_slab": "quartz_slab",
        "garden_outline": "oak_leaves",
        "garden_floor": "grass_block"
    }
    
    entranceDirection = ["N", "S", "E", "W"]
    
    for houses in rectangle_house_mountain:
        house = House(editor, houses[0], houses[1], entranceDirection[random.randint(0, 3)], blocks)
        house.build()

if __name__ == '__main__':
    main()