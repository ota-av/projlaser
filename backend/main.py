from stupidArtnet import StupidArtnetServer
from pyglet import app, clock, gl, image, window, shapes, graphics, canvas
from typing import List
from flask import Flask, request
from flask_socketio import SocketIO
import json

from os import path, makedirs

from sanitize_filename import sanitize

from copy import deepcopy

import math
    
import layer
import playback
import threading
WIDTH, HEIGHT = 16*75, 9*50

api = Flask(__name__)
api.use_reloader = False # Disable reloader to support multithread
apisocket = SocketIO(api, cors_allowed_origins="*")

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

showname: str = "default"

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
    global realtime, bpm, bpmstarttime, lock
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

@api.route('/api/save', methods=["POST"])
def save():
    global programmer, playbacks, active_playbacks, bpm, showname, lock
    filename = 'saved/' + sanitize(request.json['name']) + ".json"
    makedirs('saved', exist_ok=True)
    with open(filename, 'w') as outf:
        with lock:
            savedict = {
                'programmer': programmer,
                'playbacks': playbacks,
                'active_playbacks': active_playbacks,
                'bpm': bpm
            }
            showname = request.json['name']
            json.dump(savedict, outf)
            apisocket.emit('reload')

@api.route('/api/load', methods=["POST"])
def load():
    global programmer, playbacks, active_playbacks, bpm, showname, lock
    filename = 'saved/' + sanitize(request.json['name']) + ".json"

    if(not path.isfile(filename)):
        return 'Invalid showname', 404
    
    with open(filename, 'r') as inf:
        loadedshow = json.load(inf)
        with lock:
            programmer = loadedshow['programmer']
            playbacks = loadedshow['playbacks']
            active_playbacks = loadedshow['active_playbacks']
            bpm = loadedshow['bpm']
            showname = request.json['name']
            apisocket.emit('reload')

@api.route('/api/info')
def info():
    global showname, lock
    with lock:
        return {
            "showname": showname,
        }

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
    
@api.route('/api/programmer', methods=["DELETE"])
def clear_programmer():
    global programmer, lock
    with lock:
        programmer = playback.new_playback("programmer")
        apisocket.emit('programmer', programmer)
        return '', 200
    
@api.route('/api/record', methods=["POST"])
def record():
    global programmer, playbacks, lock
    with lock:
        pb = deepcopy(programmer)
        pb["id"] = request.json["id"]
        playbacks.append(pb)
        apisocket.emit('new_playback', pb)
        return '', 200

@api.route('/api/playback/<pb_id>/meta', methods=["PATCH"])
def on(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        for m in matches:
            if ("name" in request.json):
                m["name"] = request.json["name"]
            if ("key" in request.json):
                m["key"] = request.json["key"]
            apisocket.emit('update_playback', m)
        return '', 200

def on(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        for m in matches:
            active_playbacks.append(m)
        apisocket.emit('playback_state', {'id': pb_id, 'action': 'on'})

def off(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in active_playbacks if x["id"] == pb_id]
        for m in matches:
            active_playbacks.remove(m)
        apisocket.emit('playback_state', {'id': pb_id, 'action': 'off'})
    
@api.route('/api/bpm', methods=["POST"])
def setbpm():
    global bpm, bpmstarttime, realtime
    with lock:
        realduration = realtime - bpmstarttime
        bpmtime = realduration * bpm/60 # keep bpmtime same to keep FX in same phase etc
        bpm = request.json["bpm"]
        bpmstarttime = realtime - math.fmod(bpmtime, 0.25)*bpm*60 # keep in same /4 phase
        return '', 200

@apisocket.on('programmer')
def onProgrammer(json):
    global programmer, lock

    with lock:
        lid = json["layer"]
        param = json["param"]
        val = json["value"]
        playback.setPlaybackValue(programmer, lid, param, val)
        apisocket.emit('programmer', programmer)

@apisocket.on('playback_state')
def onPlayback(json):
    pb_id = json["id"]
    action = json["action"]
    if(action == 'off'): 
        off(pb_id=pb_id)
    if(action == 'on'): 
        on(pb_id=pb_id)

@apisocket.on('bpm')
def onbpm(json):
    global bpm, bpmstarttime, realtime
    with lock:
        realduration = realtime - bpmstarttime
        bpmtime = realduration * bpm/60 # keep bpmtime same to keep FX in same phase etc
        bpm = json["bpm"]
        bpmstarttime = realtime - math.fmod(bpmtime, 0.25)*bpm*60 # keep in same /4 phase
    
    
def run_api():
    apisocket.run(api, port=4000)

if __name__ == "__main__":
    clock.schedule_interval(update, 1/120) # schedule 60 times per second
    apithread = threading.Thread(target=run_api)
    apithread.daemon = True
    apithread.start()
    app.run()


