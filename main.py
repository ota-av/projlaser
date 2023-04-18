from stupidArtnet import StupidArtnetServer
from pyglet import app, clock, gl, image, window, shapes
import ctypes
import colorsys
from typing import List

WIDTH, HEIGHT = 1920, 1080

n = 5 # max shapes, affects DMX footprint. 9 chan per shape

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

class ShapeParams():
    def __init__(self):
        self.o = 1
        self.h = 0
        self.s = 1
        self.v = 1
        self.x = 0.5
        self.y = 0.5
        self.sizex = 0.5
        self.sizey = 0.5
        self.shape = 0

    def _rect(self, WIDTH, HEIGHT):
        width = WIDTH * self.sizex
        height = HEIGHT * self.sizey

        absx = WIDTH * self.x - width/2
        absy = HEIGHT * self.y - height/2

        return shapes.Rectangle(absx, absy, width, height)

    def get_shape(self, WIDTH, HEIGHT):
        shape = None
        if self.shape == 0:
            shape = self._rect(WIDTH, HEIGHT)
        if not shape: 
            return None
        shape.color = hsv2rgb(self.h, self.s, self.v)
        shape.opacity = round(self.o * 255)
        return shape
 
paramArray: List[ShapeParams] = []

for _ in range(n):
    paramArray.append(ShapeParams())

displayWindow = window.Window(WIDTH, HEIGHT)



def updateParams(t):
    global paramArray
    for i, param in enumerate(paramArray):
        param.h = (param.h + t*0.01) % 1
        param.sizey = 0.1
        param.sizex = 0.2
        param.x = (param.x + t*1) % 1
        if i == 0:
            param.o = 1
        else:
            param.o = 0

@displayWindow.event
def on_draw():
    global WIDTH, HEIGHT, paramArray
    displayWindow.clear()

    shape = paramArray[0].get_shape(WIDTH, HEIGHT)
    shape.draw()

if __name__ == "__main__":
    clock.schedule_interval(updateParams, 1/60) # schedule 60 times per second
    app.run()


