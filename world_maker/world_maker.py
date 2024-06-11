import World
from PIL import Image
from data_analysis import get_data, highway_map, filter_sobel, skeletonnize_map

if __name__ == '__main__':
    #world = World.World()
    #heightmap, watermap, treemap = get_data(world)
    #filter_sobel("./data/heightmap.png").save('./data/sobelmap.png')
    highway_map()
    skeletonnize_map(Image.open('./data/highwaymap.png'))
