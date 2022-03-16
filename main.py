# Task Description: https://ncl.instructure.com/courses/39977/pages/task-description-for-biocomputing?module_item_id=2232026
# Slides: http://homepages.cs.ncl.ac.uk/pawel.widera/2034/evolution/slides/art.html#/

from evol import Population, Evolution
import random


def initialize():
    # [(R,G,B,A),p1,p2,p3]
    return [random_colour(), random_point(),random_point(), random_point()]

def evaluate(x):
    return sum(x)


def select(population):
    return [random.choice(population) for i in range(2)]


def combine(*parents):
    return [a if random.random() < 0.5 else b for a, b in zip(*parents)]


def flip(x, rate):
    return [1 ^ i if random.random() < rate else i for i in x]


population = Population.generate(initialize, evaluate, size=10, maximize=True)
population.evaluate()

evolution = (Evolution().survive(fraction=0.5)
             .breed(parent_picker=select, combiner=combine)
             .mutate(mutate_function=flip, rate=0.1)
             .evaluate())

for i in range(50):
    population = population.evolve(evolution)
    print("i =", i, " best =", population.current_best.fitness,
          " worst =", population.current_worst.fitness)
