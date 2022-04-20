import random
from copy import deepcopy
from operator import attrgetter

import config


def select(population):
    selection = config.config["selection"]
    if selection["tournament size"]:
        return tournament(population)

    # if none selected
    return random.sample(population, 2)


def tournament(population):
    tournament_size = config.config["selection"]["tournament size"]
    if tournament_size > len(population):
        tournament_size = len(population)
    chosen = []
    for i in range(2):
        candidates = random.sample(population, tournament_size)
        winner = max(candidates, key=attrgetter("fitness"))  # pick by fitness
        chosen.append(deepcopy(winner))  # append a copy, not a reference
    return chosen
