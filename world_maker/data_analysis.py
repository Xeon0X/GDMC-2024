import World
from PIL import Image
from PIL import ImageFilter
import numpy as np
import networkx as nx
from scipy import ndimage
from scipy.ndimage import gaussian_gradient_magnitude
from scipy.ndimage import label
from Skeleton import Skeleton

def get_data(world: World):
    heightmap, watermap, treemap = world.getData()
    heightmap.save('./data/heightmap.png')
    watermap.save('./data/watermap.png')
    treemap.save('./data/treemap.png')
    return heightmap, watermap, treemap


def filter_inverse(image: Image) -> Image:
    """
    Invert the colors of an image.

    Args:
        image (image): image to filter
    """
    return Image.fromarray(np.invert(np.array(image)))


def filter_sobel(image) -> Image:
    """
    Edge detection algorithms from an image.

    Args:
        image (image): image to filter
    """

    # Open the image
    if isinstance(image, str):
        image = Image.open(image).convert('RGB')

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


def filter_smooth(image, radius: int = 3):
    """
    :param image: white and black image representing the derivative of the terrain (sobel), where black is flat and white is very steep.
    :param radius: Radius of the Gaussian blur.

    Returns:
        image: black or white image, with black as flat areas to be skeletonized
    """

    if isinstance(image, str):
        image = Image.open(image)

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


def remove_water_from_map(image: Image) -> Image:
    watermap = Image.open('./data/watermap.png').convert('L')

    array_heightmap = np.array(image)
    array_watermap = np.array(watermap)

    mask = array_watermap == 255
    array_heightmap[mask] = 0

    result_image = Image.fromarray(array_heightmap)
    return result_image


def group_map(image1: Image, image2: Image) -> Image:
    array1 = np.array(image1)
    array2 = np.array(image2)

    mask = array1 == 255
    array2[mask] = 255

    result_image = Image.fromarray(array2)
    return result_image


def highway_map() -> Image:
    smooth_sobel = filter_smooth("./data/sobelmap.png", 1)
    inverse_sobel = filter_inverse(smooth_sobel)
    sobel_no_water = remove_water_from_map(inverse_sobel)
    sobel_no_water.save("./data/test.png")
    array = np.array(sobel_no_water)
    array = ndimage.binary_erosion(array, iterations=10)
    array = ndimage.binary_dilation(array, iterations=5)
    image = Image.fromarray(array)
    smooth_image = filter_smooth(image, 5)
    array = np.array(smooth_image)
    array = ndimage.binary_erosion(array, iterations=17)
    image = Image.fromarray(array)
    smooth_image = filter_smooth(image, 6)
    array = np.array(smooth_image)
    array = ndimage.binary_dilation(array, iterations=3)
    image = Image.fromarray(array)
    image.save('./data/highwaymap.png')
    return image

def skeletonnize_map(map: Image):
    skeleton = Skeleton()
    image_array = np.array(map)
    skeleton.setSkeleton(image_array)
    skeleton.parseGraph()
    heightmap_skeleton, roadsArea = skeleton.map()
    heightmap_skeleton.save('./data/skeleton.png')
    roadsArea.save('./data/roads.png')