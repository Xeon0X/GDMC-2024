import World
from PIL import Image
from data_analysis import get_data, highway_map, filter_sobel, skeleton_highway_map, smooth_sobel_water, subtract_map
from City import City
from Position import Position
from random import randint

if __name__ == '__main__':
    #world = World.World()
    #heightmap, watermap, treemap = get_data(world)
    #filter_sobel("./data/heightmap.png").save('./data/sobelmap.png')
    smooth_sobel_water = smooth_sobel_water()
    #skeleton_highway_map(highway_map())
    city = City()
    for i in range(10):
        city.add_district(Position(randint(0, 400), randint(0, 400)))
    city.loop_expend_district()
    city.district_draw_map()
    city.district_generate_road()
    road = city.draw_roads(Image.new('RGB', (401, 401)),3)
    road.save('./data/roadmap.png')
    subtract_map(smooth_sobel_water,road).save('./data/roadmap2.png')
