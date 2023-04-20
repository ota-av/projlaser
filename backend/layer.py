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
    width = HEIGHT * param.get(layer.sizex, time)
    height = HEIGHT * param.get(layer.sizey, time)

    midx = WIDTH * param.get(layer.x, time)
    midy = HEIGHT * param.get(layer.y, time)

    anchorx = width / 2
    anchory = height / 2

    sh = shapes.Rectangle(midx, midy, width, height)
    sh.anchor_position = anchorx, anchory

    return sh

def _tri(layer, WIDTH, HEIGHT, time):
    width = HEIGHT * param.get(layer.sizex, time)
    height = HEIGHT * param.get(layer.sizey, time)

    midx = WIDTH * param.get(layer.x, time)
    midy = HEIGHT * param.get(layer.y, time)

    lx = midx - width / 2
    rx = midx + width / 2
    tx = midx

    ly = midy - height / 2
    ry = midy - height / 2
    ty = midy + height / 2

    return shapes.Triangle(lx, ly, rx, ry, tx, ty)

def _star(layer, WIDTH, HEIGHT, time):
    size = HEIGHT * param.get(layer.sizex, time)

    midx = WIDTH * param.get(layer.x, time)
    midy = HEIGHT * param.get(layer.y, time)


    return shapes.Star(midx,midy, size, size/10, 3)

def _circ(layer, WIDTH, HEIGHT, time):
    size = HEIGHT * param.get(layer.sizex, time)

    midx = WIDTH * param.get(layer.x, time)
    midy = HEIGHT * param.get(layer.y, time)
    return shapes.Circle(midx,midy,size)
    
def get_shape(layer: Layer, WIDTH, HEIGHT, time):
    shape = None
    if layer.type == "rect":
        shape = _rect(layer, WIDTH, HEIGHT, time)
    elif layer.type == "tri":
        shape = _tri(layer, WIDTH, HEIGHT, time)
    elif layer.type == "star":
        shape = _star(layer, WIDTH, HEIGHT, time)
    elif layer.type == "circ":
        shape = _circ(layer, WIDTH, HEIGHT, time)
    if not shape:
        return None

    shape.color = hsv2rgb(layer.hue.get(time), layer.saturation.get(time), layer.value.get(time))
    shape.opacity = round(layer.opacity.get(time) * 255)
    shape.rotation = layer.rotation * 360
    return shape

def new():
    return Layer(opacity=param.FxParam(0), hue=param.FxParam(0), saturation=param.FxParam(0), value=param.FxParam(1), x=param.FxParam(), y=param.FxParam(), sizex=param.FxParam(), sizey=param.FxParam(), rotation=param.FxParam(), type="rect")