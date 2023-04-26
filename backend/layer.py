from utils import hsv2rgb
from pyglet import shapes
from typing_extensions import TypedDict
import param

class Layer(TypedDict):
    opacity: float
    hue: float
    saturation: float
    value: float
    x: float
    y: float
    rotation: float
    sizex: float
    sizey: float
    type: str


def _rect(layer, WIDTH, HEIGHT):
    width = WIDTH * layer["sizex"]
    height = HEIGHT * layer["sizey"]

    midx = WIDTH * layer["x"]
    midy = HEIGHT * layer["y"]

    anchorx = width / 2
    anchory = height / 2

    sh = shapes.Rectangle(midx, midy, width, height)
    sh.anchor_position = anchorx, anchory

    return sh

def _tri(layer, WIDTH, HEIGHT):
    width = HEIGHT * layer["sizex"]
    height = HEIGHT * layer["sizey"]

    midx = WIDTH * layer["x"]
    midy = HEIGHT * layer["y"]

    lx = midx - width / 2
    rx = midx + width / 2
    tx = midx

    ly = midy - height / 2
    ry = midy - height / 2
    ty = midy + height / 2

    return shapes.Triangle(lx, ly, rx, ry, tx, ty)

def _star(layer, WIDTH, HEIGHT):
    size = HEIGHT * layer["sizex"]

    midx = WIDTH * layer["x"]
    midy = HEIGHT * layer["y"]


    return shapes.Star(midx,midy, size, size/10, 3)

def _circ(layer, WIDTH, HEIGHT):
    size = HEIGHT * layer["sizex"]

    midx = WIDTH * layer["x"]
    midy = HEIGHT * layer["y"]
    return shapes.Circle(midx,midy,size)
    
def get_shape(layer: Layer, WIDTH, HEIGHT):
    shape = None
    if layer["type"] == "rect":
        shape = _rect(layer, WIDTH, HEIGHT)
    elif layer["type"] == "tri":
        shape = _tri(layer, WIDTH, HEIGHT)
    elif layer["type"] == "star":
        shape = _star(layer, WIDTH, HEIGHT)
    elif layer["type"] == "circ":
        shape = _circ(layer, WIDTH, HEIGHT)
    if not shape:
        return None

    shape.color = hsv2rgb(layer["hue"], layer["saturation"], layer["value"])
    shape.opacity = round(layer["opacity"] * 255)
    shape.rotation = layer["rotation"] * 360
    return shape

def new():
    return Layer(opacity=0, hue=0, saturation=0, value=1, x=0.5, y=0.5, sizex=0.5, sizey=0.5, rotation=0, type="rect")