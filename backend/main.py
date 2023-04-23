from stupidArtnet import StupidArtnetServer
from pyglet import app, clock, gl, image, window, shapes, graphics, canvas
from typing import List
from flask import Flask, request
    
import layer
import playback
import threading
WIDTH, HEIGHT = 16*50, 9*50

api = Flask(__name__)
api.use_reloader = False # Disable reloader to support multithread

time = 0
 
display = canvas.get_display()
screens = display.get_screens()
display_window = window.Window(WIDTH, HEIGHT, fullscreen=False, screen=screens[0])

rendered_layers: list[layer.Layer] = []

layerids: list[str] = ["1", "2", "3"]

active_playbacks: list[playback.Playback] = [playback.testPlayback]
playbacks: list[playback.Playback] = []

programmer: playback.Playback = playback.new_playback("programmer")

lock = threading.Lock()

def render_playbacks():
    global rendered_layers, active_playbacks, lock, programmer
    with lock:
        rendered_layers.clear()

        for lid in layerids:
            l = layer.new()
            for pb in sorted(active_playbacks, key=lambda x: x["priority"]):
                playback.apply(pb, l, lid)

            playback.apply(programmer, l, lid)
        
            rendered_layers.append(l)

def update_time(t):
    global time
    time = time + t

def update(t):
    update_time(t)
    render_playbacks()

@display_window.event
def on_draw():
    global WIDTH, HEIGHT, activeShapes, time
    display_window.clear()

    for l in rendered_layers:
        pygletshape = layer.get_shape(l, WIDTH, HEIGHT, time)
        pygletshape.draw()

@api.route('/api/playbacks')
def list_plabacks():
    global playbacks, active_playbacks, lock
    with lock:
        return {
            "playbacks": playbacks,
            "active_ids": [x["id"] for x in active_playbacks]
        }

@api.route('/api/layers')
def list_layers():
    global layerids, lock
    with lock:
        return layerids

@api.route('/api/programmer')
def get_programmer():
    global programmer, lock
    with lock:
        return programmer
    
@api.route('/api/programmer', methods=["PATCH"])
def update_programmer():
    global programmer, lock

    if not "layerid" in request.json or not "param" in request.json or not "value" in request.json:
        return "Bad request", 400

    with lock:
        try:
            lid = request.json["layerid"]
            param = request.json["param"]
            val = request.json["value"]
            playback.setPlaybackValue(programmer, lid, param, val)
            return programmer
        except Exception as err:
            return err, 500
    
@api.route('/api/programmer', methods=["DELETE"])
def clear_programmer():
    global programmer, lock
    with lock:
        programmer = playback.new_playback("programmer")
        return programmer

def run_api():
    api.run(port=4000)

if __name__ == "__main__":
    clock.schedule_interval(update, 1/60) # schedule 60 times per second
    apithread = threading.Thread(target=run_api)
    apithread.daemon = True
    apithread.start()
    app.run()


