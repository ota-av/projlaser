from stupidArtnet import StupidArtnetServer
from pyglet import app, clock, gl, image, window, shapes, graphics
from typing import List
from shape import Shape
import defaultShapes

WIDTH, HEIGHT = 1920, 1080

time = 0
 
activeShapes: List[Shape] = []
storedShapes: List[Shape] = [defaultShapes.defaultRect, defaultShapes.rotStar, defaultShapes.rotatingLine, defaultShapes.rotatingLineOffset, defaultShapes.rectLeft, defaultShapes.rectRight]

keymap = {window.key._0: 10, window.key._1: 1, window.key._2: 2, window.key._3: 3, window.key._4: 4, window.key._5: 5, window.key._6: 6, window.key._7: 7, window.key._8: 8, window.key._9: 9}

displayWindow = window.Window(WIDTH, HEIGHT)

def updateTime(t):
    global time
    time = time + t

@displayWindow.event
def on_draw():
    global WIDTH, HEIGHT, activeShapes, time
    displayWindow.clear()

    for shape in activeShapes:
        renderShape = shape.get_shape(WIDTH, HEIGHT, time)
        renderShape.draw()

@displayWindow.event
def on_key_press(symbol, modifiers):
    if symbol in keymap:
        shapeNum = keymap[symbol] - 1
        if shapeNum < len(storedShapes):
            newShape = storedShapes[shapeNum]
        wasActive = newShape in activeShapes
        if newShape and not wasActive:
            activeShapes.append(newShape)
        else:
            activeShapes.remove(newShape)

if __name__ == "__main__":
    clock.schedule_interval(updateTime, 1/60) # schedule 60 times per second
    app.run()


