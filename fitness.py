from PIL import Image, ImageDraw, ImageChops

TARGET = Image.open("img_in/darwin.png")
MAX = 255 * TARGET.size[0] * TARGET.size[1]

def draw(solution):
    image = Image.new("RGB", (200, 200))
    canvas = ImageDraw.Draw(image,"RGBA")
    for polygon in solution:
        canvas.polygon(polygon[1:],fill=polygon[0])
    image.save("img_out/solution.png")
    return image

def evaluate(solution):
    image = draw(solution)
    diff = ImageChops.difference(image,TARGET)
    hist = diff.convert("L").histogram()
    count = sum(i*n for i,n in enumerate(hist))
    return (MAX-count)/MAX