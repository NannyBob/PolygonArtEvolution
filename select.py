import random
from copy import deepcopy
from operator import attrgetter

import config


def select(population):
    selection = config.config["selection"]
    if selection["tournament size"]:
        return tournament(population)
    else:
        return roulette(population)


def tournament(population):
    tournament_size = config.config["selection"]["tournament size"]
    if tournament_size > len(population):
        tournament_size = len(population)
    chosen = []
    for i in range(2):
        candidates = random.sample(population, tournament_size)
        winner = max(candidates, key=attrgetter("fitness"))  # pick by fitness
        chosen.append(deepcopy(winner))  # append a copy, not a reference
        population.remove(winner)
    population.append(chosen[0])
    population.append(chosen[1])
    return chosen


def roulette(population):
    # after this chooses the first individual, it is removed from the population temporarily, so as not to be chosen again
    chosen = []
    current = 0
    total = sum(indiv.fitness for indiv in population)
    pick = random.uniform(0, total)
    for individual in population:
        current += individual.fitness
        if current > pick:
            chosen.append(individual)
            population.remove(individual)

    total = sum(indiv.fitness for indiv in population)
    pick = random.uniform(0, total)
    for individual in population:
        current += individual.fitness
        if current > pick:
            chosen.append(individual)

    population.append(chosen[0])
    return chosen
