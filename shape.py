from utils import hsv2rgb
from pyglet import shapes
import math

FxFuncs = ["static", "sine", "linear"]

FxFuncMap = {
    "static": lambda x : 0,
    "sine": lambda x: math.sin(x*2*math.pi),
    "linear": lambda x: x,
    "flash": lambda x: 1 if (x < 0.5) else 0
}

class FxParam():
    def __init__(self, initial, func = "static", scale = 1, speed = 1, phase = 0):
        self.value = initial
        self.func = func
        self.phase = phase
        self.speed = speed
        self.scale = scale
    
    def get(self, time):
        return self.value + FxFuncMap[self.func]((time*self.speed + self.phase) % 1)*self.scale

class Shape():
    def __init__(self):
        self.o = FxParam(1)
        self.h = FxParam(0.6)
        self.s = FxParam(1)
        self.v = FxParam(1)
        self.x = FxParam(0.5)
        self.y = FxParam(0.5)
        self.r = FxParam(0)
        self.sizex = FxParam(0.5)
        self.sizey = FxParam(0.5)
        self.type = "rect"

    def _rect(self, WIDTH, HEIGHT, time):
        width = WIDTH * self.sizex.get(time)
        height = HEIGHT * self.sizey.get(time)

        midx = WIDTH * self.x.get(time)
        midy = HEIGHT * self.y.get(time)

        anchorx = width / 2
        anchory = height / 2

        sh = shapes.Rectangle(midx, midy, width, height)
        sh.anchor_position = anchorx, anchory

        return sh
    
    def _tri(self, WIDTH, HEIGHT, time):
        width = HEIGHT * self.sizex.get(time)
        height = HEIGHT * self.sizey.get(time)

        midx = WIDTH * self.x.get(time)
        midy = HEIGHT * self.y.get(time)

        lx = midx - width / 2
        rx = midx + width / 2
        tx = midx

        ly = midy - height / 2
        ry = midy - height / 2
        ty = midy + height / 2

        return shapes.Triangle(lx, ly, rx, ry, tx, ty)

    def _star(self, WIDTH, HEIGHT, time):
        size = HEIGHT * self.sizex.get(time)

        midx = WIDTH * self.x.get(time)
        midy = HEIGHT * self.y.get(time)


        return shapes.Star(midx,midy, size, size/10, 3)

    def get_shape(self, WIDTH, HEIGHT, time):
        renderShape = None
        if self.type == "rect":
            renderShape = self._rect(WIDTH, HEIGHT, time)
        elif self.type == "tri":
            renderShape = self._tri(WIDTH, HEIGHT, time)
        elif self.type == "star":
            renderShape = self._star(WIDTH, HEIGHT, time)
        if not renderShape:
            return None

        renderShape.color = hsv2rgb(self.h.get(time), self.s.get(time), self.v.get(time))
        renderShape.opacity = round(self.o.get(time) * 255)
        renderShape.rotation = self.r.get(time) * 360
        return renderShape