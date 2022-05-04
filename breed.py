import random

import config


def breed(*parents):
    return arithmetic_crossover(*parents)


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
                to_return.append(polygon)
    elif diff < 0:
        for polygon in parents[1][len0:len1 - 1]:
            if random.random() < 0.5:
                to_return.append(polygon)

    return to_return


def arithmetic_crossover(*parents):
    child = []
    len0 = len(parents[0])
    print(len0)
    len1 = len(parents[1])
    for i in range(min(len0, len1)):
        child.append(polygon_combine(parents[0][i], parents[1][i]))
    if len0 > len1:
        for polygon in parents[0][len1:]:
            if random.random() > 0.5:
                child.append(polygon)
    else:
        for polygon in parents[1][len0:]:
            if random.random() > 0.5:
                child.append(polygon)
    return child


def polygon_combine(a, b):
    red = round((a[0][0] + b[0][0]) / 2)
    green = round((a[0][1] + b[0][1]) / 2)
    blue = round((a[0][2] + b[0][2]) / 2)
    alpha = round((a[0][3] + b[0][3]) / 2)
    lena = len(a[1:])
    lenb = len(b[1:])
    child = [(red, green, blue, alpha)]
    for i in range(min(lena, lenb)):
        child.append(point_combine(a[i + 1], b[i + 1]))
    if lena > lenb:
        for point in a[lenb+1:]:
            if random.random() > 0.5:
                child.append(point)
    else:
        for point in b[lena+1:]:
            if random.random() > 0.5:
                child.append(point)
    return child


def point_combine(a, b):
    x = round((a[0] + b[0]) / 2)
    y = round((a[1] + b[1]) / 2)
    return x, y


def combine_random(*parents):
    combined = []
    for parent in parents:
        for polygon in parent:
            combined.append(polygon)
    to_return = random.sample(combined, int(len(combined) / 2))
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
    # pair of polygons however, if one has fewer than the other, this results in the offspring having the fewer amount.
    # this gradually decreases the number of polygons throughout the generations
    # lengths = [len(p) for p in parents]
    # if check_equal(lengths):';[
    return [a if random.random() < 0.5 else b for a, b in zip(*parents)]
