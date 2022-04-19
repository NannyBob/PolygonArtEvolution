# Task Description: https://ncl.instructure.com/courses/39977/pages/task-description-for-biocomputing?module_item_id=2232026
# Slides: http://homepages.cs.ncl.ac.uk/pawel.widera/2034/evolution/slides/art.html#/
import os

from evol import Population, Evolution
import datetime
import random
import create
import fitness
import mutate
from copy import deepcopy
from operator import attrgetter
import config

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

logging = config.config["logging"]
if logging:
    logging_folder = "img_out/full_log/" + str(datetime.datetime.now())[:19].replace(":", ".")
    os.mkdir(logging_folder)
for i in range(config.config["generations"]):
    population = population.evolve(evolution)
    print("i =", i, " best =", population.current_best.fitness,
          " worst =", population.current_worst.fitness)
    if logging:
        if (i + 1) % logging == 0:
            image = fitness.draw(population.current_best.chromosome)
            image.save(logging_folder + "/" + str(i) + ".png")

image = fitness.draw(population.current_best.chromosome)
image.save("img_out/previous best.png")
if config.config["progress"]:
    image.save(
        "img_out/progress/" + str(datetime.datetime.now())[:19].replace(":", ".") + "-" + str(config.config["generations"]) + ".png")
