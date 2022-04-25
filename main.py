# Task Description: https://ncl.instructure.com/courses/39977/pages/task-description-for-biocomputing?module_item_id=2232026
# Slides: http://homepages.cs.ncl.ac.uk/pawel.widera/2034/evolution/slides/art.html#/
import os
import shutil
import matplotlib
import matplotlib.pyplot as plt
from multiprocess.pool import Pool

from evol import Population, Evolution
import datetime
import random
import create
import fitness
import mutate
import config
import select
import breed

random.seed(1)

population = Population.generate(create.initialize, fitness.evaluate,
                                 size=config.config["population size"],
                                 maximize=True)
population.concurrent_workers = config.config["concurrent workers"]

evolution = (Evolution().survive(fraction=config.config["survival rate"])
             .breed(parent_picker=select.select,
                    combiner=breed.breed)
             .mutate(mutate_function=mutate.mutate,
                     elitist=config.config["mutation"]["elitist"])
             .evaluate(lazy=True))

logging = config.config["logging"]
if logging["log"]:
    best_fitnesses=[]
    polygon_count =[]
    worst_fitnesses=[]
    x =[]
    logging_folder = "img_out/full_log/" + str(datetime.datetime.now())[:19].replace(":", ".")
    os.mkdir(logging_folder)
    shutil.copyfile(config.filepath, logging_folder + "/" + "config.json")

for i in range(config.config["generations"]):
    population = population.evolve(evolution)
    print("i =", i, " best =", population.current_best.fitness,
          " worst =", population.current_worst.fitness)
    if logging["log"]:
        if (i + 1) % logging["interval"] == 0:
            best_fitnesses.append(population.current_best.fitness)
            worst_fitnesses.append(population.current_worst.fitness)
            polygon_count.append(len(population.current_best.chromosome))
            x.append(i+1)
            if logging["pictures"]:
                image = fitness.draw(population.current_best.chromosome)
                image.save(logging_folder + "/" + str(i+1) + ".png")

image = fitness.draw(population.current_best.chromosome)
image.save("img_out/previous best.png")
image = fitness.draw(population.current_worst.chromosome)
image.save("img_out/previous worst.png")

if logging["log"]:
    #plotting fitness
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Generations')
    ax1.set_ylabel('Fitness')
    ax1.plot(x, best_fitnesses, color='green', label = "best fitnesses")
    ax1.tick_params(axis='y', labelcolor='green')

    #plotting no of polygons
    if logging["log no of polygons"]:
        ax2 = ax1.twinx()
        ax2.tick_params(axis='y', labelcolor='blue')
        ax2.set_ylabel('Polygon Count', color='blue')
        ax2.plot(x, polygon_count, color='blue')

    if logging["log worst fitness"]:
        ax1.plot(x, worst_fitnesses, color='red', label="worst fitnesses")
    ax1.legend()
    plt.savefig(logging_folder + "/" + "graph.png")


if config.config["progress"]:
    progress_folder = "img_out/progress/" + str(datetime.datetime.now())[:19].replace(":", ".") + "-" + str(
        config.config["generations"]) + "/"
    os.mkdir(progress_folder)
    image.save(progress_folder + "image.png")
    shutil.copyfile(config.filepath, progress_folder + "config.json")
