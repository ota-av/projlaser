from pyglet import image
from utils import hsv2rgb

base = hsv2rgb(0, 0, 0.2) + (255,)
activeBase = hsv2rgb(0.55, 1, 0.4) + (255,)

def imageWithBaseColor(baseC, top):
    rtop = top.get_image_data()
    pitch = rtop.width * 4
    pixtop = rtop.get_data('RGBA', pitch)

    newData = b""
    for r,g,b,a in zip(*[iter(pixtop)]*4):
        if a == 0:
            newData += bytes(baseC)
        else:
            newData += bytes((r,g,b,a))


    im = image.create(rtop.width, rtop.height)
    im.set_data("RGBA", pitch, newData)

    return im


def activeImage(path):
    return imageWithBaseColor(activeBase, image.load(path))

def inactiveImage(path):
    return imageWithBaseColor(base, image.load(path))