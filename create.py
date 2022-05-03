import random

import config

starting_polygons = config.config["starting polygons"]


def random_colour():
    return (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))


def random_point():
    return (random.randint(0, 199), random.randint(0, 199))


def random_polygon():
    # [(R,G,B,A),p1,p2,p3]
    number_of_points = random.randint(config.config["min points"], config.config["max points"])
    points = [random_point() for i in range(number_of_points)]
    return [random_colour(), *points]


def random_solution():
    return [random_polygon() for i in range(starting_polygons)]
