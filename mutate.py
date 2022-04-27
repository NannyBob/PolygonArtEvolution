from copy import deepcopy

import config
import create
import random

import fitness


def mutate(solution):
    mutation_probs = config.config["mutation"]
    if random.random() > mutation_probs["mutation rate"]:
        return solution
    if random.random() < mutation_probs["move point"]:
        mutate_point_gaussian(solution)
    if random.random() < mutation_probs["change colour"]:
        mutate_colour_gaussian(solution)
    if random.random() < mutation_probs["add polygon"]:
        mutate_add_similar_polygon(solution)
        # mutate_add_polygon(solution)
    if random.random() < mutation_probs["remove polygon"]:
        mutate_remove_polygon(solution)
    if random.random() < mutation_probs["add point"]:
        mutate_add_point(solution)
    if random.random() < mutation_probs["remove point"]:
        mutate_remove_point(solution)

    return solution


# Maybe mutate colour and transparency seperately
def mutate_colour_gaussian(solution):
    polygon = random.choice(solution)
    polygon[0] = single_colour_gaussian(polygon[0], 10)


def mutate_point_gaussian(solution):
    polygon = random.choice(solution)
    for i in range(len(polygon[1:])):
        polygon[i + 1] = single_point_gaussian(polygon[i + 1], 10)


def mutate_add_polygon(solution):
    if len(solution) < config.config["max polygons"]:
        solution.append(create.random_polygon())


def mutate_add_similar_polygon(solution):
    if len(solution) < config.config["max polygons"]:
        polygon = random.choice(solution)
        new_polygon = deepcopy(polygon)
        if random.random() < 0.1:
            new_colour = create.random_colour()
        else:
            new_colour = single_colour_gaussian(polygon[0], 10)
        # with low alpha channel
        new_adjusted_colour = (new_colour[0], new_colour[1], new_colour[2], 10)
        new_polygon[0] = new_adjusted_colour

        for count, point in enumerate(new_polygon[1:]):
            new_polygon[count + 1] = single_point_gaussian(point, 10)
        solution.append(new_polygon)


def mutate_remove_polygon(solution):
    if len(solution) > config.config["min polygons"]:
        solution.pop(random.randint(0, len(solution) - 1))


def mutate_add_point(solution):
    polygon = random.choice(solution)
    if len(polygon) - 1 < config.config["max points"]:
        centroid = fitness.find_centroid(polygon)
        polygon.append(single_point_gaussian(centroid, 10))


def mutate_remove_point(solution):
    polygon = random.choice(solution)
    if len(polygon) - 1 > config.config["min points"]:
        polygon.pop(random.randint(config.config["min points"], len(polygon) - 1))


def single_point_gaussian(point, sigma):
    x = point[0]
    y = point[1]
    # if random.random() < indpb:
    x += random.gauss(0, sigma)
    x = max(0, min(int(x), 200))
    # if random.random() < indpb:
    y += random.gauss(0, sigma)
    y = max(0, min(int(y), 200))
    return (x, y)


def single_colour_gaussian(colour, sigma):
    r = colour[0]
    g = colour[1]
    b = colour[2]
    a = colour[3]
    if random.random() < 0.5:
        r += random.gauss(0, 10)
        r = max(0, min(int(r), 255))
    if random.random() < 0.5:
        g += random.gauss(0, 10)
        g = max(0, min(int(g), 255))
    if random.random() < 0.5:
        b += random.gauss(0, 10)
        b = max(0, min(int(b), 255))
    if random.random() < 0.5:
        a += random.gauss(0, 10)
        a = max(0, min(int(a), 255))
    return (r, g, b, a)
