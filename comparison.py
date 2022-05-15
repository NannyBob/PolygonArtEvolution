import datetime
import math
import os
import random
import sys
from multiprocessing import Pool

from matplotlib import pyplot as plt

import binary
import breed
import mutate
import select

from evol import Population, Evolution
from scipy import stats
import scikit_posthocs as sp

import config
import create
import fitness

seeds = config.config["comparison"]["seeds"]


# [pop size, mut rate, survival rate, start polygons]
def reference():
    create.starting_polygons = 53
    pop = Population.generate(create.random_solution, fitness.evaluate,
                              size=104,
                              maximize=True)
    evolution = (Evolution().survive(fraction=0.25125070269958294)
                 .breed(parent_picker=select.tournament,
                        combiner=breed.combine_pairs)
                 .mutate(mutate_function=mutate.mutate, probability=0.9447429119639668)
                 .evaluate(lazy=True))
    return pop, evolution


def arithmetic():
    create.starting_polygons = 35
    pop = Population.generate(create.random_solution, fitness.evaluate,
                              size=98,
                              maximize=True)
    evolution = (Evolution().survive(fraction=0.2)
                 .breed(parent_picker=select.tournament,
                        combiner=breed.arithmetic_crossover)
                 .mutate(mutate_function=mutate.mutate, probability=0.9501248704267389)
                 .evaluate(lazy=True))
    return pop, evolution


# [[100, 0.8053678349650185, 0.6809860539952947, 50], 0.8263800980392156]]
def roulette():
    create.starting_polygons = 50
    pop = Population.generate(create.random_solution, fitness.evaluate,
                              size=100,
                              maximize=True)
    evolution = (Evolution().survive(fraction=0.6809860539952947)
                 .breed(parent_picker=select.roulette,
                        combiner=breed.combine_pairs)
                 .mutate(mutate_function=mutate.mutate, probability=0.8053678349650185)
                 .evaluate(lazy=True))
    return pop, evolution


def bit():
    binary.starting_polygons = 50
    binary.mutation_rate = 9.7135980433153e-05
    pop = Population.generate(binary.create, binary.evaluate,
                              size=102)
    evolution = (Evolution().survive(fraction=0.8053678349650185)
                 .breed(parent_picker=select.tournament,
                        combiner=binary.crossover)
                 .mutate(mutate_function=binary.mutate)
                 .evaluate(lazy=True))
    return pop, evolution


def evolve(pop, evolution, seed):
    fitnesses = []
    random.seed(seed)
    i = 0
    while True:
        i += 1
        pop = pop.evolve(evolution)
        if i % 50 == 0:
            print(str(i) + ": " + str(pop.current_best.fitness))
            fitnesses.append(pop.current_best.fitness)
        if pop.current_best.fitness >= 0.95:
            print("under + " + str(i))
            return i, pop.current_best.chromosome, fitnesses
        if i > 30000:
            print("over")
            print(pop.current_best.fitness)
            return i + round((.95 - pop.current_best.fitness) * 20000), pop.current_best.chromosome, fitnesses


def compare():
    folder = "img_out/full_log/" + str(datetime.datetime.now())[:19].replace(":", ".")
    os.mkdir(folder)
    os.mkdir(folder + "/reference")
    os.mkdir(folder + "/arithmetic")
    os.mkdir(folder + "/roulette")
    os.mkdir(folder + "/binary")

    reference_gens = []
    arithmetic_gens = []
    roulette_gens = []
    binary_gens = []
    for seed in seeds:
    #    print(str(seed) + ": ref")
     #   pop, evolution = reference()
      #  gens, chromosome,fitnesses = evolve(pop, evolution, seed)
       # reference_gens.append(gens)
        #make_image(chromosome, folder + "/reference", seed)
        #make_graph(fitnesses, folder + "/reference", seed)

       # print(str(seed) + ": arith")
        #pop, evolution = arithmetic()
        #gens, chromosome,fitnesses = evolve(pop, evolution, seed)
        #arithmetic_gens.append(gens)
        #make_image(chromosome, folder + "/arithmetic", seed)
        #make_graph(fitnesses, folder + "/arithmetic", seed)

        #print(str(seed) + ": roul")
        #pop, evolution = roulette()
        #gens, chromosome,fitnesses = evolve(pop, evolution, seed)
        #roulette_gens.append(gens)
        #make_image(chromosome, folder + "/roulette", seed)
        #make_graph(fitnesses, folder + "/roulette", seed)

        print(str(seed) + ": binary")
        pop, evolution = bit()
        gens, chromosome,fitnesses = evolve(pop, evolution, seed)
        binary_gens.append(gens)
        make_image_binary(chromosome, folder + "/binary", seed)
        make_graph(fitnesses,folder +"/binary",seed)

    # difference between variants is only statistically significant if p < 0.05
    #print("reference data: " + str(reference_gens))
    #print("arithmetic data: " + str(arithmetic_gens))
    #print("roulette data: " + str(roulette_gens))
    print("binary data: " + str(binary_gens))
    #stat, p = stats.kruskal(reference_gens, arithmetic_gens, roulette_gens, binary_gens)
    #if p < 0.05:
    #    data = [arithmetic_gens, roulette_gens, binary_gens]
    #    p_values = sp.posthoc_dunn(data)
    #    print(p_values)
    #else:
    #    print("No statistical significance")


def make_graph(fitnesses, folder,seed):
    x = [i * 50 for i in range(len(fitnesses))]
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Generations')
    ax1.set_ylabel('Fitness')
    ax1.plot(x, fitnesses, color='red')
    plt.savefig(folder + "/" + str(seed) + "-graph.png")


def make_image(chromosome, folder, seed):
    image = fitness.draw(chromosome)
    image.save(folder + "/" + str(seed) + ".png")


def make_image_binary(chromosome, folder, seed):
    converted = binary.binary_to_solution(chromosome)
    make_image(converted, folder, seed)


if __name__ == '__main__':
    compare()
