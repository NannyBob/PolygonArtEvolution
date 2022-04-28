import random

import base
import breed
import select

from evol import Population, Evolution

# so an individual is made up of [pop size, mut rate, survival rate, start polygons]
import config
import create
import fitness
import mutate


# need to sort out starting polygons
def evaluate(solution):
    population = Population.generate(create.random_solution, fitness.evaluate,
                                     size=solution[0],
                                     maximize=True)

    evolution = (Evolution().survive(fraction=solution[2])
                 .breed(parent_picker=select.select,
                        combiner=breed.breed)
                 .mutate(mutate_function=mutate.mutate, probability=solution[1])
                 .evaluate(lazy=True))

    return base.evolve(population, evolution, 1)


def rand_individual():
    configfile = config.config
    return [mutate_population_size(configfile["population size"]),
            mutate_mutation_rate(configfile["mutation"]["mutation rate"]),
            mutate_survival_rate(configfile["survival rate"]),
            mutate_starting_polygons(configfile["starting polygons"])]


def mutate_int_gaussian(value, sigma, top, bottom):
    value += random.gauss(0, sigma)
    value = max(bottom, min(int(value), top))
    return value


def mutate_population_size(value):
    return mutate_int_gaussian(value, 5, config.config["meta"]["population max"],
                               config.config["meta"]["population min"])


def mutate_starting_polygons(value):
    return mutate_int_gaussian(value, 5, config.config["max polygons"], config.config["min polygons"])


def mutate_mutation_rate(value):
    value += random.gauss(0, 0.1)
    return max(0.0, min(value, 1.0))


def mutate_survival_rate(value):
    value += random.gauss(0, 0.1)
    return max(0.2, min(value, 0.8))


def mutate_solution(solution):
    rand = random.random()
    if rand <= 0.25:
        solution[0] = mutate_population_size(solution[0])
    elif rand <= 0.5:
        solution[1] = mutate_mutation_rate(solution[1])
    elif rand <= 0.75:
        solution[2] = mutate_survival_rate(solution[2])
    else:
        solution[3] = mutate_starting_polygons(solution[3])
    return solution


def crossover(*parents):
    child = []
    # how babies are made
    for i in range(4):
        if random.random() < 0.5:
            child.append(parents[0][i])
        else:
            child.append(parents[1][i])
    return child


population = Population.generate(rand_individual,
                                 evaluate,
                                 size=50,
                                 maximize=True)

evolution = Evolution().survive(fraction=0.5) \
    .breed(parent_picker=select.select, combiner=crossover) \
    .mutate(mutate_function=mutate_solution).evaluate(lazy=True)

for i in range(20):
    population = population.evolve(evolution)
    print(population.current_best.fitness)
