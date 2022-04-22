# Task Description: https://ncl.instructure.com/courses/39977/pages/task-description-for-biocomputing?module_item_id=2232026
# Slides: http://homepages.cs.ncl.ac.uk/pawel.widera/2034/evolution/slides/art.html#/
import os
import shutil
import matplotlib
import matplotlib.pyplot as plt

from evol import Population, Evolution
import datetime
import random
import create
import fitness
import mutate
import config
import select
import breed

population = Population.generate(create.initialize, fitness.evaluate,
                                 size=config.config["population size"],
                                 maximize=True)
population.evaluate()

evolution = (Evolution().survive(fraction=config.config["survival rate"])
             .breed(parent_picker=select.select,
                    combiner=breed.breed)
             .mutate(mutate_function=mutate.mutate,
                     elitist=config.config["mutation"]["elitist"])
             .evaluate())

logging = config.config["logging"]
if logging:
    best_fitnesses=[]
    polygon_count =[]
    x =[]
    logging_folder = "img_out/full_log/" + str(datetime.datetime.now())[:19].replace(":", ".")
    os.mkdir(logging_folder)
    shutil.copyfile(config.filepath, logging_folder + "/" + "config.json")

for i in range(config.config["generations"]):
    population = population.evolve(evolution)
    print(len(population.current_best.chromosome))
    print("i =", i, " best =", population.current_best.fitness,
          " worst =", population.current_worst.fitness)
    if logging:
        if (i + 1) % logging == 0:
            best_fitnesses.append(population.current_best.fitness)
            polygon_count.append(len(population.current_best.chromosome))
            x.append(i+1)
            image = fitness.draw(population.current_best.chromosome)
            image.save(logging_folder + "/" + str(i) + ".png")

image = fitness.draw(population.current_best.chromosome)
image.save("img_out/previous best.png")
image = fitness.draw(population.current_worst.chromosome)
image.save("img_out/previous worst.png")

if logging:
    #plotting fitness
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Generations')
    ax1.set_ylabel('Fitness', color='red')
    ax1.plot(x, best_fitnesses, color='red')
    ax1.tick_params(axis='y', labelcolor='red')

    #plotting no of polygons
    ax2 =ax1.twinx()
    ax2.set_ylabel('Polygon Count', color='blue')
    ax2.plot(x, polygon_count, color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    plt.savefig(logging_folder + "/" + "graph.png")


if config.config["progress"]:
    progress_folder = "img_out/progress/" + str(datetime.datetime.now())[:19].replace(":", ".") + "-" + str(
        config.config["generations"]) + "/"
    os.mkdir(progress_folder)
    image.save(progress_folder + "image.png")
    shutil.copyfile(config.filepath, progress_folder + "config.json")
