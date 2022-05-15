# binary representation of chromosome
# all in bytes
# colour =   (r,g,b,a) (8,8,8,8) 32
# point =    (b,x,y) (1,8,8)     17
# polygon =  (colout,point*6) (32,17*6) (135)
# polygon =  (point*100) (135*100) (13500)
import math
import random
import fitness

starting_polygons = 25
mutation_rate = 0.01


def binary_to_colour(bitstr):
    r = int(bitstr[0:8], 2)
    g = int(bitstr[8:16], 2)
    b = int(bitstr[16:24], 2)
    a = int(bitstr[24:32], 2)
    return r, g, b, a


def binary_to_point(bitstr):
    # if set as not
    if bitstr[0] == "0":
        return None
    x = int(bitstr[1:9], 2)
    if x > 200:
        diff = x - 200
        x = round(diff * (200 / 55))
    y = int(bitstr[9:17], 2)
    if y > 200:
        diff = y - 200
        y = round(diff * (200 / 55))
    return x, y


def binary_to_polygon(bitstr):
    if bitstr[0] == "0":
        return None

    polygon = [binary_to_colour(bitstr[1:33])]
    for i in range(6):
        point = binary_to_point(bitstr[33 + (i * 17):50 + (i * 17)])
        if point:
            polygon.append(point)
    if len(polygon) < 4:
        return None
    return polygon


def binary_to_solution(bitstr):
    polygons = []
    for i in range(100):
        polygon = binary_to_polygon(bitstr[0 + (135 * i):135 + (135 * i)])
        if polygon:
            polygons.append(polygon)
    return polygons


def create():
    bit_string = ""
    for i in range(13500):
        if i % 135 == 0:
            if math.floor(i / 135) <= starting_polygons:
                bit_string += '1'
            else:
                bit_string += '0'
        else:
            if random.random() > 0.5:
                bit_string += '0'
            else:
                bit_string += '1'
    return bit_string


def mutate(bitstr):
    bit_dict = {"0": "1", "1": "0"}
    newstr = ""
    for i in range(len(bitstr)):
        if random.random() < mutation_rate:
            newstr += bit_dict[bitstr[i]]
        else:
            newstr += bitstr[i]
    return newstr


def crossover(*parents):
    return ''.join([a if random.random() < 0.5 else b for a, b in zip(*parents)])


def evaluate(bitstr):
    solution = binary_to_solution(bitstr)
    fit = fitness.evaluate(solution)
    return fit
