import World
from PIL import Image
from data_analysis import get_data,filter_negative, skeleton_mountain_map, highway_map, filter_sobel, skeleton_highway_map, \
    smooth_sobel_water, subtract_map, detect_mountain
from City import City
from Position import Position
from random import randint
from pack_rectangle import generate_building

if __name__ == '__main__':
    #world = World.World()
    #heightmap, watermap, treemap = get_data(world)
    #filter_sobel("./data/heightmap.png").save('./data/sobelmap.png')
    smooth_sobel_water = smooth_sobel_water()
    skeleton_highway_map(highway_map())
    city = City()
    mountain_coo = detect_mountain()
    city.add_district(Position(mountain_coo[0], mountain_coo[1]), "mountain")
    city.add_district(Position(200, 200), "zdz")
    city.add_district(Position(300, 300), "cool")
    city.loop_expend_district()
    city.district_draw_map()
    city.district_generate_road()
    image_mountain_map = city.get_district_mountain_map()
    road = city.draw_roads(Image.new('RGB', (401, 401)), 4)
    road.save('./data/roadmap.png')
    subtract_map(smooth_sobel_water, road).save('./data/roadmap2.png')
    subtract_map('./data/roadmap2.png', './data/skeleton_highway_area.png').save('./data/roadmap2.png')
    subtract_map('./data/roadmap2.png', './data/mountain_map.png').save('./data/roadmap2.png')
    generate_building('./data/roadmap2.png')

    skeleton_mountain_map(image_mountain_map)
    subtract_map('./data/mountain_map.png','./data/skeleton_mountain_area.png').save('./data/mountain_map.png')
    subtract_map(smooth_sobel_water, filter_negative('./data/mountain_map.png')).save('./data/mountain_map.png')
    generate_building('./data/mountain_map.png')
