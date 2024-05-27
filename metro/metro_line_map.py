from Metro_Line import *
from math import pi, cos, sin, sqrt, atan2, inf
from pygame import Surface
import pygame

from metro.Metro_Line import Position


def cubic_bezier(time: float, join1: Position, control_point1: Position, control_point2: Position,
                 join2: Position) -> Position:
    """
    Calculate the position of a point on a cubic Bézier curve at a given time

    Formula used : B(t) = (1-t)^3 * P0 + 3(1-t)^2 * t * P1 + 3(1-t) * t^2 * P2 + t^3 * P3

    :param time: The time at which to calculate the position
    :param join1: The first join point of the curve
    :param control_point1: The first control point of the curve
    :param control_point2: The second control point of the curve
    :param join2: The second join point of the curve
    :return: The position of the point on the curve at the given time
    """
    return (join1 * ((1 - time) ** 3)
            + control_point1 * 3 * ((1 - time) ** 2) * time
            + control_point2 * 3 * (1 - time) * (time ** 2)
            + join2 * (time ** 3))


def cubic_bezier_derivative(time: float, join1: Position, control_point1: Position, control_point2: Position,
                            join2: Position) -> Position:
    """
    Calculate the first derivative of a cubic Bézier curve at a given time

    Formula used : B'(t) = 3(1-t)^2 * (P1 - P0) + 6(1-t) * t * (P2 - P1) + 3t^2 * (P3 - P2)

    :param time: The time at which to calculate the derivative
    :param join1: The first join point of the curve
    :param control_point1: The first control point of the curve
    :param control_point2: The second control point of the curve
    :param join2: The second join point of the curve
    :return: The derivative of the curve at the given time
    """
    return ((control_point1 - join1) * 3 * ((1 - time) ** 2)
            + (control_point2 - control_point1) * 6 * (1 - time) * time
            + (join2 - control_point2) * 3 * (time ** 2))


def cubic_bezier_second_derivative(time: float, join1: Position, control_point1: Position, control_point2: Position,
                                   join2: Position) -> Position:
    """
    Calculate the second derivative of a cubic Bézier curve at a given time

    Formula used : B''(t) = 6(1-t) * (P2 - 2P1 + P0) + 6t * (P3 - 2P2 + P1)

    :param time: The time at which to calculate the second derivative
    :param join1: The first join point of the curve
    :param control_point1: The first control point of the curve
    :param control_point2: The second control point of the curve
    :param join2: The second join point of the curve
    :return: The second derivative of the curve at the given time
    """
    return ((control_point2 - control_point1 * 2 + join1) * 6 * (1 - time)
            + (join2 - control_point2 * 2 + control_point1) * 6 * time)


def bezier_curve(control_points, num_points) -> tuple[list[Position], list[Position], list[Position]]:
    """
    Generate a Bézier curve from a list of control points

    :param control_points: The control points of the curve
    :param num_points: The number of points to generate
    :return: A tuple containing the points of the curve, the derivative of the curve,
             and the second derivative of the curve
    """
    points = []
    derivative = []
    second_derivative = []
    for t in range(num_points + 1):
        points.append(cubic_bezier(t / num_points, *control_points))
        derivative.append(cubic_bezier_derivative(t / num_points, *control_points))
        second_derivative.append(cubic_bezier_second_derivative(t / num_points, *control_points))
    return points, derivative, second_derivative


def osculating_circle(points: list[Position], derivative: list[Position], second_derivative: list[Position]) \
        -> list[tuple[int, Position]]:
    """
    Calculate the osculating circle at each point of a curve
    An osculating circle is the circle that best approximates the curve at a given point

    Source : https://en.wikipedia.org/wiki/Osculating_circle

    :param points: The points of the curve
    :param derivative: The derivative of the curve
    :param second_derivative: The second derivative of the curve
    :return: A list of tuples, each containing the radius and center of each osculating circle
    """
    circle = []
    for i in range(len(points)):
        curvature = (abs(derivative[i].x * second_derivative[i].y - derivative[i].y * second_derivative[i].x)
                     / ((derivative[i].x ** 2 + derivative[i].y ** 2) ** 1.5))
        if curvature != 0:
            radius = 1 / curvature
            normal = derivative[i].norm()
            cross_product = derivative[i].x * second_derivative[i].y - derivative[i].y * second_derivative[i].x
            if cross_product > 0:
                center = points[i] + Position(-derivative[i].y * radius / normal, derivative[i].x * radius / normal)
            else:
                center = points[i] + Position(derivative[i].y * radius / normal, -derivative[i].x * radius / normal)
            circle.append((int(radius), center))
    return circle


def merge_similar_circles(circles: list[tuple[int, Position]], radius_threshold: float, center_threshold: float) \
        -> list[tuple[int, Position]]:
    """
    Merge similar osculating circles

    :param circles: The osculating circles to merge
    :param radius_threshold: The maximum difference in radius for two circles to be considered similar
    :param center_threshold: The maximum distance between the centers of two circles to be considered similar
    :return: The merged osculating circles
    """
    merged_circles = []
    i = 0
    while i < len(circles) - 1:
        radius1, center1 = circles[i]
        radius2, center2 = circles[i + 1]
        if abs(radius1 - radius2) <= radius_threshold and center1.distance_to(center2) <= center_threshold:
            merged_radius = (radius1 + radius2) // 2
            merged_center = Position((center1.x + center2.x) // 2, (center1.y + center2.y) // 2)
            merged_circles.append((merged_radius, merged_center))
            i += 2
        else:
            merged_circles.append(circles[i])
            i += 1
    if i < len(circles):
        merged_circles.append(circles[i])

    if len(merged_circles) == len(circles):
        return merged_circles
    else:
        return merge_similar_circles(merged_circles, radius_threshold, center_threshold)


def circle_intersection(circle1: tuple[int, Position], circle2: tuple[int, Position]) -> list[Position]:
    distance = circle1[1].distance_to(circle2[1])

    if (distance > circle1[0] + circle2[0] or distance < abs(circle1[0] - circle2[0])
            or (distance == 0 and circle1[0] == circle2[0])):
        return []

    distance_line_circle = (circle1[0] ** 2 - circle2[0] ** 2 + distance ** 2) / (2 * distance)
    distance_line_intersec_point = sqrt(circle1[0] ** 2 - distance_line_circle ** 2)
    p = circle1[1] + (circle2[1] - circle1[1]) * distance_line_circle / distance

    return [Position(int(p.x + distance_line_intersec_point * (circle2[1].y - circle1[1].y) / distance),
                     int(p.y - distance_line_intersec_point * (circle2[1].x - circle1[1].x) / distance)),
            Position(int(p.x - distance_line_intersec_point * (circle2[1].y - circle1[1].y) / distance),
                     int(p.y + distance_line_intersec_point * (circle2[1].x - circle1[1].x) / distance))]


def closest_to_curve(points: list[Position], curve_points: list[Position]) -> Position:
    closest_point = Position()
    distance = inf
    for point in points:
        for curve_point in curve_points:
            distance_point_curve = point.distance_to(curve_point)
            if distance_point_curve < distance:
                distance = distance_point_curve
                closest_point = point
    return closest_point


def midpoint_circle_segment(circle: tuple[int, Position], start_point: Position, end_point: Position, curve_points: list[Position]) -> list[
    Position]:
    points = []

    start_angle = circle[1].angle_to(start_point)
    end_angle = circle[1].angle_to(end_point)

    if start_angle < 0:
        start_angle += 2 * pi
    if end_angle < 0:
        end_angle += 2 * pi
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle

    middle_angle = (start_angle+end_angle)/2
    middle_point = circle[1] + Position(int(circle[0]*cos(middle_angle)), -int(circle[0]*sin(middle_angle)))
    is_outside_point = closest_to_curve([middle_point, circle[1]], curve_points) == middle_point

    x0, y0 = circle[1].x, circle[1].y
    x = circle[0]
    y = 0
    err = 0

    while x >= y:
        for (x1, y1) in [(x0 + x, y0 + y), (x0 + y, y0 + x), (x0 - y, y0 + x), (x0 - x, y0 + y),
                         (x0 - x, y0 - y), (x0 - y, y0 - x), (x0 + y, y0 - x), (x0 + x, y0 - y)]:
            angle = atan2(y0 - y1, x1 - x0)
            if angle < 0:
                angle += 2*pi
            if is_outside_point:
                if start_angle <= angle <= end_angle:
                    points.append(Position(int(x1), int(y1)))
            else:
                if angle <= start_angle or end_angle <= angle:
                    points.append(Position(int(x1), int(y1)))

        if err <= 0:
            y += 1
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1

    return points


def calculate_control_points(station, next_station, curve_factor) -> tuple[Position, Position]:
    """
    Calculate the control points for a Bézier curve between two stations

    :param station: The first station
    :param next_station: The second station
    :param curve_factor: The factor to multiply the distance between stations to create the control points
    :return: A tuple containing the control points for the curve
    """
    distance = station.distance_to(next_station)

    control_point_pos = station.pos + Position(cos(station.orientation) * distance * curve_factor,
                                               -sin(station.orientation) * distance * curve_factor)

    control_point_next_pos = next_station.pos + Position(
        cos(next_station.orientation + pi) * distance * curve_factor,
        - sin(next_station.orientation + pi) * distance * curve_factor)

    return control_point_pos, control_point_next_pos


def metro_line_osculating_circles(metro: Metro_Line, curve_factor: float = 0.5, num_points_factor: float = 1 / 20) -> (
        tuple)[list[tuple[int, Position]], list[Position]]:
    """
    Calculate the osculating circles of a metro line

    :param metro: The metro line to calculate the osculating circles of
    :param curve_factor: How much the control points should be offset from the stations
    :param num_points_factor: How many points to generate for each segment of the curve
    :return: A tuple containing the osculating circles and the points of the metro line curve
    """
    print(f"[METRO LINE] Calculating osculating circles of the metro line {metro.name}")
    circles = []
    points_list = []
    for i in range(len(metro.stations) - 1):
        print(f"[METRO LINE] Calculating between {metro.stations[i].name} and {metro.stations[i].next_station.name}")
        station = metro.stations[i]

        distance = station.distance_to(station.next_station)

        control_point_pos, control_point_next_pos = calculate_control_points(station, station.next_station,
                                                                             curve_factor)

        points, derivatives, second_derivatives = bezier_curve(
            [station.pos, control_point_pos, control_point_next_pos, station.next_station.pos],
            int(distance * num_points_factor))

        osculating_circles = osculating_circle(points, derivatives, second_derivatives)
        merged_circles = merge_similar_circles(osculating_circles, 50, 50)
        print(
            f"[METRO LINE] {len(osculating_circles) - len(merged_circles)} out of {len(osculating_circles)} circles deleted !")
        circles.extend(merged_circles)
        points_list.extend(points)
    print(f"[METRO LINE] Osculating circles done")
    return circles, points_list


# --- DRAW PART ---

def draw_osculating_circle(circle: list[tuple[int, Position]], surface: Surface):
    """
    :param circle: The osculating circles to draw
    :param surface: The surface on which to draw the circles
    """
    for radius, center in circle:
        pygame.draw.circle(surface, (255, 0, 0), (center.x, center.y), int(radius), 1)
        pygame.draw.circle(surface, (0, 0, 255), (center.x, center.y), 10)


def draw_station(station: Station, surface: Surface):
    """
    :param station: The station to draw
    :param surface: The surface on which to draw the station
    """
    pygame.draw.circle(surface, (255, 255, 255), (station.pos.x, station.pos.y), 10)


def draw_points(points: list[Position], surface):
    """
    :param points: The points to draw
    :param surface: The surface on which to draw the points
    """
    for point in points:
        pygame.draw.circle(surface, (40, 255, 40), (point.x, point.y), 5)


def draw_point(point: Position, surface):
    pygame.draw.circle(surface, (40, 255, 40), (point.x, point.y), 5)


def draw_pixels(points: list[Position], surface):
    for point in points:
        surface.set_at((point.x, point.y), (0, 255, 255))


def draw_metro_line(metro: Metro_Line, surface: Surface, show_points: bool = True):
    """
    :param metro: The metro line to draw
    :param surface: The surface on which to draw the metro line
    :param show_points: Whether to show the points of the curve
    """
    for i in range(len(metro.stations) - 1):
        station = metro.stations[i]
        draw_station(station, surface)
        draw_station(station.next_station, surface)

    circles, points = metro_line_osculating_circles(metro)
    draw_osculating_circle(circles, surface)
    for i in range(1, len(circles) - 1):
        intersect_point_circle_before = closest_to_curve(circle_intersection(circles[i - 1], circles[i]), points)
        intersect_point_circle_after = closest_to_curve(circle_intersection(circles[i], circles[i + 1]), points)
        if intersect_point_circle_before == Position():
            continue
            intersect_point_circle_before = circles[i - 1][1]
        else:
            draw_point(intersect_point_circle_before, surface)

        if intersect_point_circle_after == Position():
            continue
            intersect_point_circle_after = circles[i + 1][1]
        else:
            draw_point(intersect_point_circle_after, surface)

        points_midpoint = midpoint_circle_segment(circles[i], intersect_point_circle_before,
                                                  intersect_point_circle_after, points)
        draw_pixels(points_midpoint, surface)

    if len(points) != 0:
        intersect_point_circle_before = points[0]
        intersect_point_circle_after = closest_to_curve(circle_intersection(circles[0], circles[1]), points)
        points_midpoint = midpoint_circle_segment(circles[0], intersect_point_circle_before,
                                                  intersect_point_circle_after, points)
        draw_pixels(points_midpoint, surface)

        intersect_point_circle_before = points[-1]
        intersect_point_circle_after = closest_to_curve(circle_intersection(circles[-1], circles[-2]), points)
        points_midpoint = midpoint_circle_segment(circles[-1], intersect_point_circle_before,
                                                  intersect_point_circle_after, points)
        draw_pixels(points_midpoint, surface)


def interface():
    """
    Interface for creating a metro line

    Control :

    - Up arrow ↑ Create a station facing north

    - Down arrow ↓ Create a station facing south

    - Left arrow ← Create a station facing west

    - Right arrow → Create a station facing east
    """
    metro = Metro_Line('A')
    surface = pygame.display.set_mode((1000, 1000))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                angle = 0
                if event.key == pygame.K_UP:
                    angle = pi / 2
                elif event.key == pygame.K_DOWN:
                    angle = -pi / 2
                elif event.key == pygame.K_LEFT:
                    angle = pi
                x, y = pygame.mouse.get_pos()
                metro.add_station(Station(Position(x, y), angle, str(len(metro.stations))))
                draw_metro_line(metro, surface)

        pygame.display.flip()


def main():
    interface()


if __name__ == "__main__":
    main()
