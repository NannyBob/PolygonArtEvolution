# Task Description: https://ncl.instructure.com/courses/39977/pages/task-description-for-biocomputing?module_item_id=2232026
# Slides: http://homepages.cs.ncl.ac.uk/pawel.widera/2034/evolution/slides/art.html#/

from evol import Population, Evolution
import random
import fitness
import mutation

init_polygons = 50


def random_colour():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def random_point():
    return random.randint(0, 200), random.randint(0, 200)


def rand_polygon():
    # [(R,G,B,A),p1,p2,p3]
    return [random_colour(), random_point(), random_point(), random_point()]




def initialize():
    return [rand_polygon() for i in range(init_polygons)]


def select(pop):
    return [random.choice(pop) for _ in range(2)]


def combine(*parents):
    return [a if random.random() < 0.5 else b for a, b in zip(*parents)]


population = Population.generate(initialize, fitness.evaluate, size=10, maximize=True)
population.evaluate()

evolution = (Evolution()
             .survive(fraction=0.5)
             .breed(parent_picker=select, combiner=combine)
             .mutate(mutate_function=mutation.mutate)
             .evaluate())

for i in range(100):
    population = population.evolve(evolution)
    print("i =", i, " best =", population.current_best.fitness,
          " worst =", population.current_worst.fitness)
