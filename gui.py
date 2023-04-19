from pyglet import app, clock, gl, image, window, shapes, gui, graphics
import images

guiWindow = window.Window(1080, 720)
guiBatch = graphics.Batch()
frame = gui.Frame(guiWindow, order=4)

params = ["type", "pos"]

paramButtons = {}

selectedParam = "type"

@guiWindow.event
def on_draw():
    guiWindow.clear()
    guiBatch.draw()

def setActiveParam(self):
    for param in paramButtons:
        paramButtons[param].value = False
    paramButtons[self].value = True

for i, param in enumerate(params):
    pb = gui.PushButton(0+i*128,128,images.activeImage(f'img/sel_{param}.png'),images.inactiveImage(f'img/sel_{param}.png'), batch=guiBatch)
    pb.set_handler('on_release', lambda x=param: setActiveParam(x))
    paramButtons[param] = pb
    frame.add_widget(pb)