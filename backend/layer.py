from utils import hsv2rgb
from pyglet import shapes
from typing_extensions import TypedDict
import param

class Layer(TypedDict):
    opacity: param.FxParam
    hue: param.FxParam
    saturation: param.FxParam
    value: param.FxParam
    x: param.FxParam
    y: param.FxParam
    rotation: param.FxParam
    sizex: param.FxParam
    sizey: param.FxParam
    type: str


def _rect(layer, WIDTH, HEIGHT, time):
    width = HEIGHT * param.get(layer["sizex"], time)
    height = HEIGHT * param.get(layer["sizey"], time)

    midx = WIDTH * param.get(layer["x"], time)
    midy = HEIGHT * param.get(layer["y"], time)

    anchorx = width / 2
    anchory = height / 2

    sh = shapes.Rectangle(midx, midy, width, height)
    sh.anchor_position = anchorx, anchory

    return sh

def _tri(layer, WIDTH, HEIGHT, time):
    width = HEIGHT * param.get(layer["sizex"], time)
    height = HEIGHT * param.get(layer["sizey"], time)

    midx = WIDTH * param.get(layer["x"], time)
    midy = HEIGHT * param.get(layer["y"], time)

    lx = midx - width / 2
    rx = midx + width / 2
    tx = midx

    ly = midy - height / 2
    ry = midy - height / 2
    ty = midy + height / 2

    return shapes.Triangle(lx, ly, rx, ry, tx, ty)

def _star(layer, WIDTH, HEIGHT, time):
    size = HEIGHT * param.get(layer["sizex"], time)

    midx = WIDTH * param.get(layer["x"], time)
    midy = HEIGHT * param.get(layer["y"], time)


    return shapes.Star(midx,midy, size, size/10, 3)

def _circ(layer, WIDTH, HEIGHT, time):
    size = HEIGHT * param.get(layer["sizex"], time)

    midx = WIDTH * param.get(layer["x"], time)
    midy = HEIGHT * param.get(layer["y"], time)
    return shapes.Circle(midx,midy,size)
    
def get_shape(layer: Layer, WIDTH, HEIGHT, time):
    shape = None
    if layer["type"] == "rect":
        shape = _rect(layer, WIDTH, HEIGHT, time)
    elif layer["type"] == "tri":
        shape = _tri(layer, WIDTH, HEIGHT, time)
    elif layer["type"] == "star":
        shape = _star(layer, WIDTH, HEIGHT, time)
    elif layer["type"] == "circ":
        shape = _circ(layer, WIDTH, HEIGHT, time)
    if not shape:
        return None

    shape.color = hsv2rgb(param.get(layer["hue"], time), param.get(layer["saturation"], time), param.get(layer["value"], time))
    shape.opacity = round(param.get(layer["opacity"], time) * 255)
    shape.rotation = param.get(layer["rotation"], time) * 360
    return shape

def new():
    return Layer(opacity=param.new(0), hue=param.new(0), saturation=param.new(0), value=param.new(1), x=param.new(0.5), y=param.new(0.5), sizex=param.new(0.5), sizey=param.new(0.5), rotation=param.new(), type="rect")