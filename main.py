# Task Description: https://ncl.instructure.com/courses/39977/pages/task-description-for-biocomputing?module_item_id=2232026
# Slides: http://homepages.cs.ncl.ac.uk/pawel.widera/2034/evolution/slides/art.html#/

from evol import Population, Evolution
import datetime
import random
import create
import fitness
import mutate
from copy import deepcopy
from operator import attrgetter

generations = 10000

def select(population):
    chosen = []
    for i in range(2):
        candidates = random.sample(population, 5)
        winner = max(candidates, key=attrgetter("fitness"))  # pick by fitness
        chosen.append(deepcopy(winner))  # append a copy, not a reference
    return chosen


def combine(*parents):
    return [a if random.random() < 0.5 else b for a, b in zip(*parents)]


population = Population.generate(create.initialize, fitness.evaluate, size=10, maximize=True)
population.evaluate()

evolution = (Evolution().survive(fraction=0.5)
             .breed(parent_picker=select, combiner=combine)
             .mutate(mutate_function=mutate.mutate, rate=0.1)
             .evaluate())

for i in range(generations):
    population = population.evolve(evolution)
    print("i =", i, " best =", population.current_best.fitness,
          " worst =", population.current_worst.fitness)

image = fitness.draw(population.current_best.chromosome)
image.save("img_out/previous best.png")
image.save("progress/" + str(datetime.datetime.now().time())[:8].replace(":", ".") + "-" +str(generations)+".png")
