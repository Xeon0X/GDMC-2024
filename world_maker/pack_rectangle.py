from PIL import Image
import numpy as np
from typing import Union
from world_maker.data_analysis import handle_import_image
from random import randint


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Bin:
    def __init__(self, grid):
        self.grid = grid
        self.rectangles = []

    def place_rectangle(self, rectangle):
        best_spot = None
        best_spot_empty_area = float('inf')

        for i in range(len(self.grid[0]) - rectangle.width + 1):
            for j in range(len(self.grid) - rectangle.height + 1):
                if self.can_place(rectangle, i, j):
                    empty_area = self.calculate_empty_area(rectangle, i, j)
                    if empty_area < best_spot_empty_area:
                        best_spot = (i, j)
                        best_spot_empty_area = empty_area

        if best_spot is not None:
            self.rectangles.append(
                (best_spot, (best_spot[0] + rectangle.width, best_spot[1] + rectangle.height)))
            self.update_grid(rectangle, *best_spot)
            return True

        return False

    def calculate_empty_area(self, rectangle, x, y):
        empty_area = 0
        for rect_x in range(x, x + rectangle.width):
            for rect_y in range(y, y + rectangle.height):
                if self.grid[rect_y][rect_x]:
                    empty_area += 1
        return empty_area

    def can_place(self, rectangle, x, y):
        for rect_x in range(x, x + rectangle.width):
            for rect_y in range(y, y + rectangle.height):
                if not self.grid[rect_y][rect_x]:
                    return False
        return True

    def update_grid(self, rectangle, x, y):
        for rect_x in range(x, x + rectangle.width):
            for rect_y in range(y, y + rectangle.height):
                self.grid[rect_y][rect_x] = False


def generate_rectangle(min_width: int = 10, max_width: int = 25):
    width = randint(min_width, max_width)
    height = randint(min_width, max_width)
    return Rectangle(width, height)


def pack_rectangles(grid, min_width: int = 10, max_width: int = 25):
    bin = Bin(grid)
    while True:
        rectangle = generate_rectangle(min_width, max_width)
        if not bin.place_rectangle(rectangle):
            break
    return bin.rectangles


def draw_rectangles(rectangles, grid, heightmap):
    heightmap = handle_import_image(heightmap).convert('L')
    image = Image.new('L', (len(grid[0]), len(grid)), 0)
    for rectangle in rectangles:
        start, end = rectangle
        height = []
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                height.append(heightmap.getpixel((x, y)))
        height_average = sum(height)/len(height)
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                image.putpixel((x, y), round(height_average))
    return image


def area_of_rectangles(rectangles):
    area = 0
    for rectangle in rectangles:
        start, end = rectangle
        area += abs((end[0] - start[0]) * (end[1] - start[1]))
    return area


def generate_building(image: str | Image.Image, heightmap: str | Image.Image, output: str = './world_maker/data/building.png',
                      number_of_try: int = 3, min_width: int = 10, max_width: int = 25):
    print("[Building] Start generating building position...")
    image = handle_import_image(image).convert('L')
    rectangles_output = []
    for n in range(number_of_try):
        print("[Building] Try", n+1)
        grid = np.array(image)
        rectangles = pack_rectangles(grid, min_width, max_width)
        print("[Building] Number of building:", len(rectangles))
        print("[Building] Area of building:", area_of_rectangles(rectangles))
        if area_of_rectangles(rectangles) > area_of_rectangles(rectangles_output):
            rectangles_output = rectangles
    draw_rectangles(rectangles_output, grid, heightmap).save(output)
    return rectangles_output
