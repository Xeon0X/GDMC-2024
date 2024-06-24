from world_maker.World import World
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage
from world_maker.Skeleton import Skeleton
from world_maker.Position import Position
from random import randint, choice
import cv2


def get_data(world: World):
    print("[Data Analysis] Generating data...")
    heightmap, watermap, treemap = world.getData()
    heightmap.save('./world_maker/data/heightmap.png')
    watermap.save('./world_maker/data/watermap.png')
    treemap.save('./world_maker/data/treemap.png')
    print("[Data Analysis] Data generated.")
    return heightmap, watermap, treemap


def get_data_no_update():
    print("[Data Analysis] Generating data...")
    # heightmap, watermap, treemap = world.getData()
    heightmap, watermap, treemap = handle_import_image(
        './world_maker/data/heightmap.png'), handle_import_image(
        './world_maker/data/watermap.png'), handle_import_image(
        './world_maker/data/treemap.png')
    print("[Data Analysis] Data generated.")
    return heightmap, watermap, treemap


def handle_import_image(image: str | Image.Image) -> Image.Image:
    if isinstance(image, str):
        return Image.open(image)
    return image


def filter_negative(image: str | Image.Image) -> Image.Image:
    """
    Invert the colors of an image.

    Args:
        image (image): image to filter
    """
    image = handle_import_image(image)
    return Image.fromarray(np.invert(np.array(image)))


def filter_sobel(image: str | Image.Image) -> Image.Image:
    """
    Edge detection algorithms from an image.

    Args:
        image (image): image to filter
    """

    # Open the image
    image = handle_import_image(image).convert('RGB')

    img = np.array(image).astype(np.uint8)

    # Apply gray scale
    gray_img = np.round(
        0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    ).astype(np.uint8)

    # Sobel Operator
    h, w = gray_img.shape
    # define filters
    horizontal = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])  # s2
    vertical = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])  # s1

    # define images with 0s
    newhorizontalImage = np.zeros((h, w))
    newverticalImage = np.zeros((h, w))
    newgradientImage = np.zeros((h, w))

    # offset by 1
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            horizontalGrad = (
                (horizontal[0, 0] * gray_img[i - 1, j - 1])
                + (horizontal[0, 1] * gray_img[i - 1, j])
                + (horizontal[0, 2] * gray_img[i - 1, j + 1])
                + (horizontal[1, 0] * gray_img[i, j - 1])
                + (horizontal[1, 1] * gray_img[i, j])
                + (horizontal[1, 2] * gray_img[i, j + 1])
                + (horizontal[2, 0] * gray_img[i + 1, j - 1])
                + (horizontal[2, 1] * gray_img[i + 1, j])
                + (horizontal[2, 2] * gray_img[i + 1, j + 1])
            )

            newhorizontalImage[i - 1, j - 1] = abs(horizontalGrad)

            verticalGrad = (
                (vertical[0, 0] * gray_img[i - 1, j - 1])
                + (vertical[0, 1] * gray_img[i - 1, j])
                + (vertical[0, 2] * gray_img[i - 1, j + 1])
                + (vertical[1, 0] * gray_img[i, j - 1])
                + (vertical[1, 1] * gray_img[i, j])
                + (vertical[1, 2] * gray_img[i, j + 1])
                + (vertical[2, 0] * gray_img[i + 1, j - 1])
                + (vertical[2, 1] * gray_img[i + 1, j])
                + (vertical[2, 2] * gray_img[i + 1, j + 1])
            )

            newverticalImage[i - 1, j - 1] = abs(verticalGrad)

            # Edge Magnitude
            mag = np.sqrt(pow(horizontalGrad, 2.0) + pow(verticalGrad, 2.0))
            newgradientImage[i - 1, j - 1] = mag

    image = Image.fromarray(newgradientImage)
    image = image.convert("L")

    return image


def filter_smooth_theshold(image: str | Image.Image, radius: int = 3):
    """
    :param image: white and black image representing the derivative of the terrain (sobel), where black is flat and white is very steep.
    :param radius: Radius of the Gaussian blur.

    Returns:
        image: black or white image, with black as flat areas to be skeletonized
    """

    image = handle_import_image(image)

    # image = image.filter(ImageFilter.SMOOTH_MORE)
    # image = image.filter(ImageFilter.SMOOTH_MORE)
    # image = image.filter(ImageFilter.SMOOTH_MORE)
    image = image.convert('L')
    image = image.filter(ImageFilter.GaussianBlur(radius))
    array = np.array(image)

    bool_array = array > 7

    # bool_array = ndimage.binary_opening(bool_array, structure=np.ones((3,3)), iterations=1)
    # bool_array = ndimage.binary_closing(bool_array, structure=np.ones((3,3)), iterations=1)
    # bool_array = ndimage.binary_opening(bool_array, structure=np.ones((5,5)), iterations=1)
    # bool_array = ndimage.binary_closing(bool_array, structure=np.ones((5,5)), iterations=1)
    # bool_array = ndimage.binary_opening(bool_array, structure=np.ones((7,7)), iterations=1)
    # bool_array = ndimage.binary_closing(bool_array, structure=np.ones((7,7)), iterations=1)

    return Image.fromarray(bool_array)


def filter_smooth(image: str | Image.Image, radius: int = 3):
    image = handle_import_image(image)
    image = image.convert('L')
    image = image.filter(ImageFilter.GaussianBlur(radius))
    return image


def subtract_map(image: str | Image.Image, substractImage: str | Image.Image) -> Image.Image:
    image = handle_import_image(image)
    substractImage = handle_import_image(substractImage).convert('L')

    array_heightmap = np.array(image)
    array_substractImage = np.array(substractImage)

    mask = array_substractImage == 255
    array_heightmap[mask] = 0

    return Image.fromarray(array_heightmap)


def overide_map(base: Image, top: Image) -> Image.Image:
    base = handle_import_image(base).convert('L')
    top = handle_import_image(top).convert('L')

    width, height = base.size

    if top.size != (width, height):
        raise ValueError("Mismatching images sizes")

    result_image = Image.new('L', (width, height))

    for x in range(width):
        for y in range(height):
            base_pixel = base.getpixel((x, y))
            top_pixel = top.getpixel((x, y))

            if top_pixel != 0:
                result_image.putpixel((x, y), top_pixel)
            else:
                result_image.putpixel((x, y), base_pixel)

    return result_image


def group_map(image1: str | Image.Image, image2: str | Image.Image) -> Image.Image:
    image1 = handle_import_image(image1).convert('L')
    image2 = handle_import_image(image2).convert('L')

    array1 = np.array(image1)
    array2 = np.array(image2)

    mask = array1 == 255
    array2[mask] = 255

    return Image.fromarray(array2)


def filter_smooth_array(array: np.ndarray, radius: int = 3) -> np.ndarray:
    image = Image.fromarray(array)
    smooth_image = filter_smooth_theshold(image, radius)
    array = np.array(smooth_image)
    return array


def filter_remove_details(image: str | Image.Image, n: int = 20) -> Image.Image:
    image = handle_import_image(image)
    array = np.array(image)
    for _ in range(n):
        array = ndimage.binary_dilation(array, iterations=4)
        array = ndimage.binary_erosion(array, iterations=5)
        array = filter_smooth_array(array, 2)
        array = ndimage.binary_erosion(array, iterations=3)
    image = Image.fromarray(array)
    return image


def highway_map() -> Image.Image:
    print("[Data Analysis] Generating highway map...")
    smooth_sobel = filter_smooth_theshold("./world_maker/data/sobelmap.png", 1)
    negative_smooth_sobel = filter_negative(smooth_sobel)
    negative_smooth_sobel_water = subtract_map(
        negative_smooth_sobel, './world_maker/data/watermap.png')
    array_sobel_water = np.array(negative_smooth_sobel_water)
    array_sobel_water = ndimage.binary_erosion(
        array_sobel_water, iterations=12)
    array_sobel_water = ndimage.binary_dilation(
        array_sobel_water, iterations=5)
    array_sobel_water = filter_smooth_array(array_sobel_water, 5)
    array_sobel_water = ndimage.binary_erosion(
        array_sobel_water, iterations=20)
    array_sobel_water = filter_smooth_array(array_sobel_water, 6)
    image = Image.fromarray(array_sobel_water)
    image_no_details = filter_remove_details(image, 15)
    image_no_details.save('./world_maker/data/highwaymap.png')
    print("[Data Analysis] Highway map generated.")
    return image_no_details


def create_volume(surface: np.ndarray, heightmap: np.ndarray, make_it_flat: bool = False) -> np.ndarray:
    volume = np.full((len(surface[0]), 255, len(surface)), False)
    for z in range(len(surface)):
        for x in range(len(surface[0])):
            if not make_it_flat:
                volume[x][heightmap[z][x]][z] = surface[z][x]
            else:
                volume[x][0][z] = surface[z][x]
    return volume


def convert_2D_to_3D(image: str | Image.Image, make_it_flat: bool = False) -> np.ndarray:
    image = handle_import_image(image)
    heightmap = Image.open(
        './world_maker/data/heightmap_smooth.png').convert('L')
    heightmap = np.array(heightmap)
    surface = np.array(image)
    volume = create_volume(surface, heightmap, make_it_flat)
    return volume


def skeleton_highway_map(image: str | Image.Image = './world_maker/data/highwaymap.png') -> Skeleton:
    image_array = convert_2D_to_3D(image, True)
    skeleton = Skeleton(image_array)
    skeleton.parse_graph(True)
    heightmap_skeleton = skeleton.map()
    heightmap_skeleton.save('./world_maker/data/skeleton_highway.png')
    skeleton.road_area('skeleton_highway_area.png', 10)
    return skeleton


def skeleton_mountain_map(image: str | Image.Image = './world_maker/data/mountain_map.png') -> Skeleton:
    image_array = convert_2D_to_3D(image, True)
    skeleton = Skeleton(image_array)
    skeleton.parse_graph()
    heightmap_skeleton = skeleton.map()
    heightmap_skeleton.save('./world_maker/data/skeleton_mountain.png')
    skeleton.road_area('skeleton_mountain_area.png', 3)
    return skeleton


def smooth_sobel_water() -> Image.Image:
    watermap = handle_import_image("./world_maker/data/watermap.png")
    watermap = filter_negative(
        filter_remove_details(filter_negative(watermap), 5))
    sobel = handle_import_image("./world_maker/data/sobelmap.png")
    sobel = filter_remove_details(filter_smooth_theshold(sobel, 1), 2)
    group = group_map(watermap, sobel)
    group = filter_negative(group)
    group.save('./world_maker/data/smooth_sobel_watermap.png')
    return group


def mountain_map_expend(mountain_map: list[list[int]], starting_point: tuple[int, int], value: int):
    explore_points = [starting_point]
    while len(explore_points) > 0:
        x, y = explore_points.pop(0)
        mountain_map[y][x] = value
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (0 <= x + i < len(mountain_map[0]) and 0 <= y + j < len(mountain_map) and
                        mountain_map[y + j][x + i] == 0):
                    if (x + i, y + j) not in explore_points:
                        explore_points.append((x + i, y + j))


def set_values_of_building_mountain(mountain_map: list[list[int]], area_mountain: list[int],
                                    building_map: str | Image.Image = "./world_maker/data/smooth_sobel_watermap.png"):
    building_map = handle_import_image(building_map).convert('L')
    for y in range(building_map.size[1]):
        for x in range(building_map.size[0]):
            if building_map.getpixel((x, y)) > 144:
                if mountain_map[y][x] != -1:
                    area_mountain[mountain_map[y][x] - 1] += 1


def get_index_of_biggest_area_mountain(area_mountain: list[int], exception: list[int]) -> int:
    max_value = -1
    index = -1
    for i in range(len(area_mountain)):
        if i not in exception and area_mountain[i] > max_value:
            max_value = area_mountain[i]
            index = i
    return index


def get_random_point_in_area_mountain(mountain_map: list[list[int]], index: int) -> Position | None:
    points = []
    for y in range(len(mountain_map)):
        for x in range(len(mountain_map[0])):
            if mountain_map[y][x] == index + 1:
                points.append(Position(x, y))
    if not points:
        return None
    return choice(points)


def get_center_of_area_mountain(mountain_map: list[list[int]], index: int) -> Position:
    sum_x = 0
    sum_y = 0
    count = 0
    for y in range(len(mountain_map)):
        for x in range(len(mountain_map[0])):
            if mountain_map[y][x] == index + 1:
                sum_x += x
                sum_y += y
                count += 1
    center = Position(sum_x // count, sum_y // count)
    if mountain_map[center.y][center.x] != index + 1:
        return get_random_point_in_area_mountain(mountain_map, index)
    return center


def detect_mountain(number_of_mountain: int = 2, height_threshold: int = 10,
                    image_heightmap: str | Image.Image = './world_maker/data/heightmap.png') -> list[Position]:
    print("[Data Analysis] Detecting mountains...")
    image_heightmap = handle_import_image(image_heightmap).convert('L')

    avg_height = 0
    for y in range(image_heightmap.size[1]):
        for x in range(image_heightmap.size[0]):
            avg_height += image_heightmap.getpixel((x, y))
    avg_height = int(
        avg_height / (image_heightmap.size[0] * image_heightmap.size[1]))
    print("[Data Analysis] Average height:", avg_height)

    mountain_map = [[-1 if image_heightmap.getpixel((x, y)) < (avg_height + height_threshold) else 0 for x in
                     range(image_heightmap.size[0])] for y in
                    range(image_heightmap.size[1])]

    area_mountain = []
    for y in range(image_heightmap.size[1]):
        for x in range(image_heightmap.size[0]):
            if mountain_map[y][x] == 0:
                area_mountain.append(0)
                mountain_map_expend(mountain_map, (x, y), len(area_mountain))

    if not area_mountain:
        print("[Data Analysis] No mountain detected.")
        return []

    set_values_of_building_mountain(mountain_map, area_mountain)
    if number_of_mountain < len(area_mountain):
        index_mountain = []
        for n in range(number_of_mountain):
            index_mountain.append(get_index_of_biggest_area_mountain(
                area_mountain, index_mountain))
    else:
        index_mountain = [i for i in range(len(area_mountain))]

    position_mountain = []
    for i in range(len(index_mountain)):
        position_mountain.append(get_center_of_area_mountain(
            mountain_map, index_mountain[i]))

    return position_mountain


def rectangle_2D_to_3D(rectangle: list[tuple[tuple[int, int], tuple[int, int]]],
                       height_min: int = 6, height_max: int = 10) \
        -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    image = handle_import_image(
        './world_maker/data/heightmap.png').convert('L')
    new_rectangle = []
    for rect in rectangle:
        start, end = rect
        height = {}
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                if image.getpixel((x, y)) not in height:
                    height[image.getpixel((x, y))] = 1
                else:
                    height[image.getpixel((x, y))] += 1
        max_height = max(height, key=height.get)
        new_rectangle.append(
            ((start[0], max_height, start[1]), (end[0], max_height + randint(height_min, height_max), end[1])))
    return new_rectangle


def transpose_form_heightmap(heightmap: str | Image.Image, coordinates, origin: tuple[int, int]) -> tuple[
        int, int, int]:
    heightmap = handle_import_image(heightmap).convert('L')

    xMin, zMin = origin

    return (coordinates[0] + xMin, heightmap.getpixel(
        (coordinates[0], coordinates[-1])), coordinates[-1] + zMin)
