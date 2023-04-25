from stupidArtnet import StupidArtnetServer
from pyglet import app, clock, gl, image, window, shapes, graphics, canvas
from typing import List
from flask import Flask, request

from copy import deepcopy

import math
    
import layer
import playback
import threading
WIDTH, HEIGHT = 16*75, 9*50

api = Flask(__name__)
api.use_reloader = False # Disable reloader to support multithread

realtime = 0
bpmstarttime = 0
bpm = 120
 
display = canvas.get_display()
screens = display.get_screens()
display_window = window.Window(WIDTH, HEIGHT, fullscreen=False, screen=screens[0])

rendered_layers: list[layer.Layer] = []

layerids: list[str] = ["1", "2", "3", "4"]

active_playbacks: list[playback.Playback] = []
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
    global realtime
    realtime = realtime + t

def update(t):
    update_time(t)
    render_playbacks()

def get_bpm_time():
    global realtime, bpm, bpmstarttime
    with lock:
        realduration = realtime - bpmstarttime
        bpmduration = realduration * bpm/60
        return bpmduration

@display_window.event
def on_draw():
    global WIDTH, HEIGHT, rendered_layers
    display_window.clear()

    bpmtime = get_bpm_time()

    for l in rendered_layers:
        pygletshape = layer.get_shape(l, WIDTH, HEIGHT, bpmtime)
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

    if not "layer" in request.json or not "param" in request.json or not "value" in request.json:
        return "Bad request", 400

    with lock:
        try:
            lid = request.json["layer"]
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
    
@api.route('/api/record', methods=["POST"])
def record():
    global programmer, playbacks, lock
    with lock:
        pb = deepcopy(programmer)
        pb["id"] = request.json["id"]
        playbacks.append(pb)
        return pb

@api.route('/api/playback/<pb_id>/on', methods=["POST"])
def on(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        print(playbacks[0]['id'], type(playbacks[0]['id']), pb_id, type(pb_id), matches, pb_id)
        for m in matches:
            active_playbacks.append(m)
        return [x["id"] for x in active_playbacks]

@api.route('/api/playback/<pb_id>/off', methods=["POST"])
def off(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in active_playbacks if x["id"] == pb_id]
        for m in matches:
            active_playbacks.remove(m)
        return [x["id"] for x in active_playbacks]
    
@api.route('/api/bpm', methods=["POST"])
def setbpm():
    global bpm, bpmstarttime, realtime
    with lock:
        realduration = realtime - bpmstarttime
        bpmtime = realduration * bpm/60 # keep bpmtime same to keep FX in same phase etc
        bpm = request.json["bpm"]
        bpmstarttime = realtime - math.fmod(bpmtime, 0.25)*bpm*60 # keep in same /4 phase
        return '', 200

def run_api():
    api.run(port=4000)

if __name__ == "__main__":
    clock.schedule_interval(update, 1/120) # schedule 60 times per second
    apithread = threading.Thread(target=run_api)
    apithread.daemon = True
    apithread.start()
    app.run()


