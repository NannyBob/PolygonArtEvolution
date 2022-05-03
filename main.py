from datetime import datetime
import os
import random
import shutil
import json

from matplotlib import pyplot as plt

import base
import breed
import select

from evol import Population, Evolution

# so an individual is made up of [pop size, mut rate, survival rate, start polygons]
import config
import create
import fitness
import mutate

seed = int(round(datetime.now().timestamp()))


# need to sort out starting polygons
def evaluate(solution):
    random.seed(seed)
    print(solution)
    create.starting_polygons = solution[3]
    pop = Population.generate(create.random_solution, fitness.evaluate,
                              size=solution[0],
                              maximize=True)

    evol = (Evolution().survive(fraction=solution[2])
            .breed(parent_picker=select.select,
                   combiner=breed.breed)
            .mutate(mutate_function=mutate.mutate, probability=solution[1])
            .evaluate(lazy=True))
    fit = base.evolve(pop, evol)

    # to maintain randomness in all other sections of the meta-evolution
    random.seed(int(round(datetime.now().timestamp())))
    return fit


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
    return mutate_int_gaussian(value, 5, config.config["population max"],
                               config.config["population min"])


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
                                 size=config.config["meta"]["population size"],
                                 maximize=True)

evolution = Evolution().survive(fraction=config.config["meta"]["survival rate"]) \
    .breed(parent_picker=select.select, combiner=crossover) \
    .mutate(mutate_function=mutate_solution, probability=config.config["meta"]["mutation rate"]).evaluate(lazy=True)

best_of = []
for i in range(config.config["meta"]["generations"]):
    seed = i
    print(i)
    population = population.evolve(evolution)
    best_of.append(population.current_best)
    print(population.current_best.chromosome)

folder = "img_out/full_log/" + str(datetime.now())[:19].replace(":", ".") + "/"
os.mkdir(folder)
x = [i for i in range(config.config["meta"]["generations"])]
fig, ax1 = plt.subplots()
ax1.set_xlabel('Generations')
ax1.set_ylabel('Fitness')
ax1.plot(x, [i.fitness for i in best_of], color='red')
plt.savefig(folder + "fitness.png")

fig, ax1 = plt.subplots()
ax1.set_xlabel('Generations')
ax1.set_ylabel('Mutation Rate')
ax1.plot(x, [i.chromosome[1] for i in best_of], color='orange')
plt.savefig(folder + "mutation.png")

fig, ax1 = plt.subplots()
ax1.set_xlabel('Generations')
ax1.set_ylabel('Survival Rate')
ax1.plot(x, [i.chromosome[2] for i in best_of], color='orange')
plt.savefig(folder + "survival.png")

fig, ax1 = plt.subplots()
ax1.set_xlabel('Generations')
ax1.set_ylabel('Population Size')
ax1.plot(x, [i.chromosome[0] for i in best_of], color='orange')
plt.savefig(folder + "population size.png")

fig, ax1 = plt.subplots()
ax1.set_xlabel('Generations')
ax1.set_xlabel('Starting Polygons')
ax1.plot(x, [i.chromosome[3] for i in best_of], color='orange')
plt.savefig(folder + "polygons.png")

with open(folder + 'output.txt', 'w') as filehandle:
    json.dump([i.chromosome for i in best_of], filehandle)
shutil.copyfile(config.filepath, folder + "config.json")
