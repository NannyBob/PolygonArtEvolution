import random

import config


def breed(*parents):
    breed_dict = config.config["breed"]
    if breed_dict["combine pairs"]:
        return combine_pairs(*parents)
    elif breed_dict["combine random"]:
        return combine_random(*parents)
    elif breed_dict["crossover"]:
        return crossover(*parents)


def combine_pairs(*parents):
    # assumes two parents
    to_return = [a if random.random() < 0.5 else b for a, b in zip(*parents)]

    # if one is longer than the other, adds on extra
    len0 = len(parents[0])
    len1 = len(parents[1])
    diff = len0 - len1
    if diff > 0:
        for polygon in parents[0][len1:len0 - 1]:
            if random.random() < 0.5:
                print("fixed1")
                to_return.append(polygon)
    elif diff < 0:
        for polygon in parents[1][len0:len1 - 1]:
            if random.random() < 0.5:
                print("fixed2")
                to_return.append(polygon)

    return to_return


def combine_random(*parents):
    combined = []
    for parent in parents:
        for polygon in parent:
            combined.append(polygon)
    to_return = random.sample(combined, 2)
    return to_return


def crossover(*parents):
    # for polygon in zip(*parents):
    return parents[0]


def check_equal(lst):
    first = lst[0]
    for elem in lst:
        if elem != first:
            return False
    return True


def combine_pairs_original(*parents):
    # creates offspring by combining the polygons from the two parents, picks randomly between the polygons for each
    # pair of polygons however, if one has few than the other, this results in the offspring having the fewer amount.
    # this gradually decreases the number of polygons throughout the generations
    # lengths = [len(p) for p in parents]
    # if check_equal(lengths):';[
    return [a if random.random() < 0.5 else b for a, b in zip(*parents)]
