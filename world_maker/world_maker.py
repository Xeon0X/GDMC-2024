import World
from PIL import Image
from data_analysis import get_data,filter_negative, rectangle_2D_to_3D, skeleton_mountain_map, highway_map, filter_sobel, skeleton_highway_map, \
    smooth_sobel_water, subtract_map, detect_mountain
from City import City
from Position import Position
from random import randint
from pack_rectangle import generate_building

if __name__ == '__main__':
    #world = World.World()
    #heightmap, watermap, treemap = get_data(world)
    #filter_sobel("./world_maker/data/heightmap.png").save('./world_maker/data/sobelmap.png')
    smooth_sobel_water = smooth_sobel_water()
    skeleton_highway_map(highway_map())
    city = City()
    city.generate_district()
    city.loop_expend_district()
    city.district_draw_map()
    city.district_generate_road()
    image_mountain_map = city.get_district_mountain_map()
    road = city.draw_roads(4)
    road.save('./world_maker/data/roadmap.png')
    subtract_map(smooth_sobel_water, road).save('./world_maker/data/city_map.png')
    subtract_map('./world_maker/data/city_map.png', './world_maker/data/skeleton_highway_area.png').save('./world_maker/data/city_map.png')
    subtract_map('./world_maker/data/city_map.png', './world_maker/data/mountain_map.png').save('./world_maker/data/city_map.png')
    rectangle_building = generate_building('./world_maker/data/city_map.png')
    rectangle_building = rectangle_2D_to_3D(rectangle_building)

    skeleton_mountain_map(image_mountain_map)
    subtract_map('./world_maker/data/mountain_map.png', './world_maker/data/skeleton_mountain_area.png').save('./world_maker/data/mountain_map.png')
    subtract_map(smooth_sobel_water, filter_negative('./world_maker/data/mountain_map.png')).save('./world_maker/data/mountain_map.png')
    rectangle_mountain = generate_building('./world_maker/data/mountain_map.png')
