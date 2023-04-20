from stupidArtnet import StupidArtnetServer
from pyglet import app, clock, gl, image, window, shapes, graphics, canvas
from typing import List
from layer import Layer
import defaultShapes

WIDTH, HEIGHT = 1920, 1080

time = 0
 
activeShapes: List[Layer] = []
storedShapes: List[Layer] = [defaultShapes.rectUpdown, defaultShapes.rotStar, defaultShapes.rotatingLine, defaultShapes.rotatingLineOffset, defaultShapes.rectLeft, defaultShapes.rectRight, defaultShapes.blackmid]

keymap = {window.key._0: 10, window.key._1: 1, window.key._2: 2, window.key._3: 3, window.key._4: 4, window.key._5: 5, window.key._6: 6, window.key._7: 7, window.key._8: 8, window.key._9: 9}

display = canvas.get_display()
screens = display.get_screens()
displayWindow = window.Window(WIDTH, HEIGHT, fullscreen=True, screen=screens[0])

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


