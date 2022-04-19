from PIL import Image, ImageDraw, ImageChops
from math import atan


TARGET = Image.open("img_in/darwin.png")
MAX = 255 * TARGET.size[0] * TARGET.size[1]

def draw(solution):
    image = Image.new("RGB", (200, 200))
    canvas = ImageDraw.Draw(image,"RGBA")
    for polygon in solution:
        #points = point_order(polygon)
        points = polygon[1:]
        canvas.polygon(points,fill=polygon[0])
    return image

def evaluate(solution):
    image = draw(solution)
    diff = ImageChops.difference(image,TARGET)
    hist = diff.convert("L").histogram()
    count = sum(i*n for i,n in enumerate(hist))
    return (MAX-count)/MAX

def point_order(polygon):
    points = polygon[1:]
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    centroid = (sum(x) / len(points), sum(y) / len(points))
    sorted(points, key=sort_func(5,centroid=centroid))
    return points


def sort_func(x, centroid):
    return atan(x,centroid)
