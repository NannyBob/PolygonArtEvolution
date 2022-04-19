import config
import create
import random


def mutate(solution, rate):
    mutation_probs = config.config["mutation"]
    if random.random() < mutation_probs["move point"]:
        mutate_point_gaussian(solution, rate)
    if random.random() < mutation_probs["change colour"]:
        mutate_colour_gaussian(solution)
    if random.random() < mutation_probs["add polygon"]:
        mutate_add_polygon(solution)
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
    polygon[0] = single_colour_gaussian(polygon[0])
    return solution


def mutate_point_gaussian(solution, indpb):
    polygon = random.choice(solution)
    for i in range(len(polygon[1:])):
        polygon[i + 1] = single_point_gaussian(polygon[i + 1], indpb)
    return solution


def mutate_add_polygon(solution):
    if len(solution) < config.config["max polygons"]:
        solution.append(create.random_polygon())
    return solution


def mutate_remove_polygon(solution):
    if len(solution) > config.config["min polygons"]:
        solution.pop(random.randint(0, len(solution) - 1))
    return solution


def mutate_add_point(solution):
    polygon = random.choice(solution)
    if len(solution) + 1 < config.config["max points"]:
        solution.append(create.random_point())
    return solution


def mutate_remove_point(solution):
    polygon = random.choice(solution)
    if len(solution) + 1 < config.config["min points"]:
        solution.pop(random.randint(config.config["min points"], len(polygon) - 1))
    return solution


def single_point_gaussian(point, indpb):
    x = point[0]
    y = point[1]
    if random.random() < indpb:
        x += random.gauss(0, 10)
        x = max(0, min(int(x), 200))
    if random.random() < indpb:
        y += random.gauss(0, 10)
        y = max(0, min(int(y), 200))
    return (x, y)


def single_colour_gaussian(colour):
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
