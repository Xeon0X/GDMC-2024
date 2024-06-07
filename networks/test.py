from gdpc import Editor, Block, geometry


def cirlce(xm, ym, r):
    editor = Editor(buffering=True)
    x = -r
    y = 0
    err = 2-2*r
    while (True):
        editor.placeBlock((round(xm-x), 102, round(ym+y)),
                          Block("white_concrete"))
        editor.placeBlock((round(xm-y), 102, round(ym-x)),
                          Block("red_concrete"))
        editor.placeBlock((round(xm+x), 102, round(ym-y)),
                          Block("blue_concrete"))
        editor.placeBlock((round(xm+y), 102, round(ym+x)),
                          Block("green_concrete"))
        print(xm-x, ym+y)
        print(xm-y, ym-x)
        print(xm+x, ym-y)
        print(xm+y, ym+x)
        r = err
        if (r <= y):
            y += 1
            err += y*2+1
        if (r > x or err > y):
            x += 1
            err += x*2+1
        if (x < 0):
            continue
        else:
            break


print("\n")
cirlce(-1606, 758, 20)


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = z
        self.z = y

    def __repr__(self):
        return f"({self.x} {self.y} {self.z})"


def drawLineOverlap(start, end, overlap):
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

    if (delta_x > delta_y):
        error = delta_2y - delta_x
        while (start.x != end.x):
            start.x += step_x
            if (error >= 0):
                if (overlap == 'LINE_OVERLAP_MAJOR'):
                    print(start.x, start.y)

                start.y += step_y
                if (overlap == 'LINE_OVERLAP_MINOR'):
                    print(start.x - step_x, start.y)
                error -= delta_2x
            error += delta_2y
            print(start.x, start.y)
    else:
        error = delta_2x - delta_y
        while (start.y != end.y):
            start.y += step_y
            if (error >= 0):
                if (overlap == 'LINE_OVERLAP_MAJOR'):
                    print(start)
                start.x += step_x
                if (overlap == 'LINE_OVERLAP_MINOR'):
                    print(start.x, start.y - step.y)
                error -= delta_2y
            error += delta_2x
            print(start.x, start.y)


drawLineOverlap(Point(-10, 0, 0,), Point(10, 0, 3), "None")
