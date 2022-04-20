import random

import config


def breed(*parents):
    breed_dict = config.config["breed"]
    if breed_dict["combine"]:
        return combine(*parents)
    elif breed_dict["crossover"]:
        return crossover(*parents)


def combine(*parents):
    return [a if random.random() < 0.5 else b for a, b in zip(*parents)]


def crossover(*parents):
    return parents[0]
