import random
import main
import create

def remove_polygon(solution):
    if len(solution > 1):
        return solution.pop(random.randint(0, len(solution) - 1))
    return solution


def add_polygon(solution):
    solution.append(create.random_polygon())
    return solution

def add_point(solution):
    # http://homepages.cs.ncl.ac.uk/pawel.widera/2034/evolution/slides/art.html#/representation/0
    polygon = random.choice(solution)

def mutate(solution):
    if random.random() < 0.5:
        remove_polygon(solution)
    else:
        add_polygon(solution)
    return solution
