import random

import config


def random_colour():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def random_point():
    return (random.randint(0, 199), random.randint(0, 199))


def random_polygon():
    # [(R,G,B,A),p1,p2,p3]
    return [random_colour(), random_point(), random_point(), random_point()]


def initialize():
    return [random_polygon() for i in range(config.config["population size"])]
