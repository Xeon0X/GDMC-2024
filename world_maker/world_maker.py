import World
from PIL import Image
from data_analysis import get_data, highway_map, filter_sobel, skeleton_highway_map

if __name__ == '__main__':
    world = World.World()
    heightmap, watermap, treemap = get_data(world)
    filter_sobel("./data/heightmap.png").save('./data/sobelmap.png')
    skeleton_highway_map(highway_map())
