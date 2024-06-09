from gdpc import Editor, Block, geometry
from enum import Enum
import random


def circle(xm, ym, r, pixel_perfect=True):
    editor = Editor(buffering=True)
    block = random.choices(("white_concrete", "red_concrete", "blue_concrete", "green_concrete",
                           "yellow_concrete", "black_concrete", "purple_concrete", "pink_concrete"))[0]
    x = -r
    y = 0
    err = 2-2*r
    while (True):
        editor.placeBlock((xm-x, 141, ym+y),
                          Block(block))
        editor.placeBlock((xm-y, 141, ym-x),
                          Block(block))
        editor.placeBlock((xm+x, 141, ym-y),
                          Block(block))
        editor.placeBlock((xm+y, 141, ym+x),
                          Block(block))
        print(xm-x, ym+y)
        print(xm-y, ym-x)
        print(xm+x, ym-y)
        print(xm+y, ym+x)
        r = err
        update = False
        if (r <= y):
            y += 1
            update = True
            err += y*2+1
        if ((r > x or err > y)):
            if (pixel_perfect == True or update == False):
                x += 1
                err += x*2+1
                update = True
        if (x < 0):
            continue
        else:
            break


def set_pixel(x, y, colour):
    editor = Editor(buffering=True)
    editor.placeBlock((x, 160, y),
                      Block(colour))


def x_line(x1, x2, y, colour):
    while x1 <= x2:
        set_pixel(x1, y, colour)
        x1 += 1


def y_line(x, y1, y2, colour):
    while y1 <= y2:
        set_pixel(x, y1, colour)
        y1 += 1


def circle2(xc, yc, inner, outer):
    # https://stackoverflow.com/questions/27755514/circle-with-thickness-drawing-algorithm
    xo = outer
    xi = inner
    y = 0
    erro = 1 - xo
    erri = 1 - xi

    while xo >= y:
        colour = random.choices(("white_concrete", "red_concrete", "blue_concrete", "green_concrete",
                                "yellow_concrete", "black_concrete", "purple_concrete", "pink_concrete"))[0]
        x_line(xc + xi, xc + xo, yc + y,  colour)
        y_line(xc + y,  yc + xi, yc + xo, colour)
        x_line(xc - xo, xc - xi, yc + y,  colour)
        y_line(xc - y,  yc + xi, yc + xo, colour)
        x_line(xc - xo, xc - xi, yc - y,  colour)
        y_line(xc - y,  yc - xo, yc - xi, colour)
        x_line(xc + xi, xc + xo, yc - y,  colour)
        y_line(xc + y,  yc - xo, yc - xi, colour)

        y += 1

        if erro < 0:
            erro += 2 * y + 1
        else:
            xo -= 1
            erro += 2 * (y - xo + 1)

        if y > inner:
            xi = y
        else:
            if erri < 0:
                erri += 2 * y + 1
            else:
                xi -= 1
                erri += 2 * (y - xi + 1)


# print("\n")
# circle2(-1606, 758, 5, 15)
# circle2(-1606, 758, 5, 5)
# circle2(-1606, 758, 10, 10)
circle2(-1606, 758, 15, 17)


class LineOverlap(Enum):
    NONE = 0
    MAJOR = 1
    MINOR = 2


class LineThicknessMode(Enum):
    MIDDLE = 0
    DRAW_COUNTERCLOCKWISE = 1
    DRAW_CLOCKWISE = 2


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x} {self.y})"

    def copy(self):
        return Point2D(self.x, self.y)

    def get_coordinates(self):
        return (self.x, self.y)


def drawLineOverlap(start, end, overlap):
    y = 120
    block = random.choices(("white_concrete", "red_concrete", "blue_concrete", "green_concrete",
                           "yellow_concrete", "black_concrete", "purple_concrete", "pink_concrete"))[0]
    print(block)
    editor = Editor(buffering=True)

    start = start.copy()
    end = end.copy()

    # Direction
    delta_x = end.x - start.x
    delta_y = end.y - start.y

    if (delta_x < 0):
        delta_x = -delta_x
        step_x = -1
    else:
        step_x = +1

    if (delta_y < 0):
        delta_y = -delta_y
        step_y = -1
    else:
        step_y = +1

    delta_2x = 2*delta_x
    delta_2y = 2*delta_y

    print(start.x, start.y)
    editor.placeBlock((start.x, y, start.y), Block(block))

    if (delta_x > delta_y):
        error = delta_2y - delta_x
        while (start.x != end.x):
            start.x += step_x
            if (error >= 0):
                if (overlap == LineOverlap.MAJOR):
                    print(start.x, start.y)
                    editor.placeBlock((start.x, y, start.y),
                                      Block(block))

                start.y += step_y
                if (overlap == LineOverlap.MINOR):
                    print(start.x - step_x, start.y)
                    editor.placeBlock((start.x - step_x, y, start.y),
                                      Block(block))
                error -= delta_2x
            error += delta_2y
            print(start.x, start.y)
            editor.placeBlock((start.x, y, start.y),
                              Block(block))
    else:
        error = delta_2x - delta_y
        while (start.y != end.y):
            start.y += step_y
            if (error >= 0):
                if (overlap == LineOverlap.MAJOR):
                    print(start)
                    editor.placeBlock((start.x, y, start.y),
                                      Block(block))
                start.x += step_x
                if (overlap == LineOverlap.MINOR):
                    print(start.x, start.y - step.y, start.z, )
                    editor.placeBlock((start.x, y, start.y - step.y),
                                      Block(block))
                error -= delta_2y
            error += delta_2x
            print(start.x, start.y)
            editor.placeBlock((start.x, y, start.y),
                              Block("white_concrete"))


# drawLineOverlap(Point2D(-10, 0, 0,), Point2D(10, 0, 3),
#                 LineOverlap.NONE)


def drawThickLine(start, end, thickness, thickness_mode):
    delta_y = end.x - start.x
    delta_x = end.y - start.y

    print("START", start)

    swap = True
    if delta_x < 0:
        delta_x = -delta_x
        step_x = -1
        swap = not swap
    else:
        step_x = +1

    if (delta_y < 0):
        delta_y = -delta_y
        step_y = -1
        swap = not swap
    else:
        step_y = +1

    delta_2x = 2 * delta_x
    delta_2y = 2 * delta_y

    draw_start_adjust_count = int(thickness / 2)
    if (thickness_mode == LineThicknessMode.DRAW_COUNTERCLOCKWISE):
        draw_start_adjust_count = thickness - 1
    elif (thickness_mode == LineThicknessMode.DRAW_CLOCKWISE):
        draw_start_adjust_count = 0
    print("START", start)
    if (delta_x >= delta_y):
        if swap:
            draw_start_adjust_count = (thickness - 1) - draw_start_adjust_count
            step_y = -step_y
        else:
            step_x = -step_x

        error = delta_2y - delta_x
        for i in range(draw_start_adjust_count, 0, -1):
            print("START", start)
            start.x -= step_x
            end.x -= step_x
            if error >= 0:
                start.y -= step_y
                end.y -= step_y
                error -= delta_2x
            error += delta_2x
        print("START", start)
        print("First print")
        print(start, end)
        drawLineOverlap(start, end, LineOverlap.NONE)
        print(start, end)
        print("End print")

        error = delta_2x - delta_x
        for i in range(thickness, 1, -1):
            start.x += step_x
            end.x += step_x
            overlap = LineOverlap.NONE
            if (error >= 0):
                start.y += step_y
                end.y += step_y
                error -= delta_2x
                overlap = LineOverlap.MAJOR
            error += delta_2y
            print("Second print")
            print(start, end)
            drawLineOverlap(start, end, overlap)
            print(start, end)
            print("End print")
    else:
        if swap:
            step_x = -step_x
        else:
            draw_start_adjust_count = (thickness - 1) - draw_start_adjust_count
            step_y = -step_y

        error = delta_2x - delta_y
        for i in range(draw_start_adjust_count, 0, -1):
            start.y -= step_y
            end.y -= step_y
            if (error >= 0):
                start.x -= step_x
                end.x -= step_x
                error -= delta_2y
            error += delta_2x

        print("Third line")
        print(start, end)
        drawLineOverlap(start, end, LineOverlap.NONE)
        print(start, end)
        print("End line")
        error = delta_2x - delta_y
        for i in range(thickness, 1, -1):
            start.y += step_y
            end.y += step_y
            overlap = LineOverlap.NONE
            if (error >= 0):
                start.x += step_x
                end.x += step_x
                error -= delta_2y
                overlap = LineOverlap.MAJOR
            error += delta_2x
            print("Fourth line")
            print(start, end)
            drawLineOverlap(start, end, overlap)
            print(start, end)
            print("End")


print("SPACE\n\n")
drawThickLine(Point2D(-1681, 864), Point2D(-1804, 920),
              21,  LineThicknessMode.MIDDLE)
