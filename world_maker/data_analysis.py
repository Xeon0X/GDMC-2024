import World
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage
from Skeleton import Skeleton
from typing import Union
from random import randint
import cv2


def get_data(world: World):
    print("[Data Analysis] Generating data...")
    heightmap, watermap, treemap = world.getData()
    heightmap.save('./world_maker/data/heightmap.png')
    watermap.save('./world_maker/data/watermap.png')
    treemap.save('./world_maker/data/treemap.png')
    print("[Data Analysis] Data generated.")
    return heightmap, watermap, treemap


def handle_import_image(image: Union[str, Image]) -> Image:
    if isinstance(image, str):
        return Image.open(image)
    return image


def filter_negative(image: Union[str, Image]) -> Image:
    """
    Invert the colors of an image.

    Args:
        image (image): image to filter
    """
    image = handle_import_image(image)
    return Image.fromarray(np.invert(np.array(image)))


def filter_sobel(image: Union[str, Image]) -> Image:
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


def filter_smooth(image: Union[str, Image], radius: int = 3):
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


def subtract_map(image: Union[str, Image], substractImage: Union[str, Image]) -> Image:
    image = handle_import_image(image)
    substractImage = handle_import_image(substractImage).convert('L')

    array_heightmap = np.array(image)
    array_substractImage = np.array(substractImage)

    mask = array_substractImage == 255
    array_heightmap[mask] = 0

    return Image.fromarray(array_heightmap)


def group_map(image1: Union[str, Image], image2: Union[str, Image]) -> Image:
    image1 = handle_import_image(image1).convert('L')
    image2 = handle_import_image(image2).convert('L')

    array1 = np.array(image1)
    array2 = np.array(image2)

    mask = array1 == 255
    array2[mask] = 255

    return Image.fromarray(array2)


def filter_smooth_array(array: np.ndarray, radius: int = 3) -> np.ndarray:
    image = Image.fromarray(array)
    smooth_image = filter_smooth(image, radius)
    array = np.array(smooth_image)
    return array


def filter_remove_details(image: Union[str, Image], n: int = 20) -> Image:
    image = handle_import_image(image)
    array = np.array(image)
    for _ in range(n):
        array = ndimage.binary_dilation(array, iterations=4)
        array = ndimage.binary_erosion(array, iterations=5)
        array = filter_smooth_array(array, 2)
        array = ndimage.binary_erosion(array, iterations=3)
    image = Image.fromarray(array)
    return image


def highway_map() -> Image:
    print("[Data Analysis] Generating highway map...")
    smooth_sobel = filter_smooth("./world_maker/data/sobelmap.png", 1)
    negative_smooth_sobel = filter_negative(smooth_sobel)
    negative_smooth_sobel_water = subtract_map(negative_smooth_sobel, './world_maker/data/watermap.png')
    array_sobel_water = np.array(negative_smooth_sobel_water)
    array_sobel_water = ndimage.binary_erosion(array_sobel_water, iterations=12)
    array_sobel_water = ndimage.binary_dilation(array_sobel_water, iterations=5)
    array_sobel_water = filter_smooth_array(array_sobel_water, 5)
    array_sobel_water = ndimage.binary_erosion(array_sobel_water, iterations=20)
    array_sobel_water = filter_smooth_array(array_sobel_water, 6)
    image = Image.fromarray(array_sobel_water)
    image_no_details = filter_remove_details(image, 15)
    image_no_details.save('./world_maker/data/highwaymap.png')
    print("[Data Analysis] Highway map generated.")
    return image_no_details


def create_volume(surface: np.ndarray, heightmap: np.ndarray, make_it_flat: bool = False) -> np.ndarray:
    volume = np.full((len(surface), 255, len(surface[0])), False)
    for z in range(len(surface)):
        for x in range(len(surface[0])):
            if not make_it_flat:
                volume[x][heightmap[z][x]][z] = surface[z][x]
            else:
                volume[x][0][z] = surface[z][x]
    return volume


def convert_2D_to_3D(image: Union[str, Image], make_it_flat: bool = False) -> np.ndarray:
    image = handle_import_image(image)
    heightmap = Image.open('./world_maker/data/heightmap.png').convert('L')
    heightmap = np.array(heightmap)
    surface = np.array(image)
    volume = create_volume(surface, heightmap, make_it_flat)
    return volume


def skeleton_highway_map(image: Union[str, Image] = './world_maker/data/highwaymap.png') -> Skeleton:
    image_array = convert_2D_to_3D(image, True)
    skeleton = Skeleton(image_array)
    skeleton.parse_graph(True)
    heightmap_skeleton = skeleton.map()
    heightmap_skeleton.save('./world_maker/data/skeleton_highway.png')
    skeleton.road_area('skeleton_highway_area.png', 10)
    return skeleton


def skeleton_mountain_map(image: Union[str, Image] = './world_maker/data/mountain_map.png') -> Skeleton:
    image_array = convert_2D_to_3D(image, True)
    skeleton = Skeleton(image_array)
    skeleton.parse_graph()
    heightmap_skeleton = skeleton.map()
    heightmap_skeleton.save('./world_maker/data/skeleton_mountain.png')
    skeleton.road_area('skeleton_mountain_area.png',3)
    return skeleton


def smooth_sobel_water() -> Image:
    watermap = handle_import_image("./world_maker/data/watermap.png")
    watermap = filter_negative(filter_remove_details(filter_negative(watermap), 5))
    sobel = handle_import_image("./world_maker/data/sobelmap.png")
    sobel = filter_remove_details(filter_smooth(sobel, 1), 2)
    group = group_map(watermap, sobel)
    group = filter_negative(group)
    group.save('./world_maker/data/smooth_sobel_watermap.png')
    return group


def detect_mountain(image: Union[str, Image] = './world_maker/data/sobelmap.png') -> Image:
    image = handle_import_image(image)
    sobel = np.array(image)
    pixels = sobel.reshape((-1, 1))
    pixels = np.float32(pixels)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = 3
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(sobel.shape)
    mountain = segmented_image == segmented_image.max()

    contours, _ = cv2.findContours(mountain.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(max_contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    print(f"[Data Analysis] The center of the mountain is at ({cX}, {cY})")
    return (cX, cY)


def rectangle_2D_to_3D(rectangle: list[tuple[tuple[int, int],tuple[int, int]]],
                       height_min:int = 6, height_max:int = 10) \
        -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    image = handle_import_image('./world_maker/data/heightmap.png')
    new_rectangle = []
    for rect in rectangle:
        start, end = rect
        avg_height = 0
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                avg_height += np.array(image.getpixel((x, y)))
        avg_height = int(avg_height / ((end[0] - start[0]) * (end[1] - start[1])))
        new_rectangle.append(((start[0], avg_height, start[1]), (end[0], avg_height + randint(height_min, height_max), end[1])))
    return new_rectangle

