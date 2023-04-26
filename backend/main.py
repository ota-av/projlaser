from stupidArtnet import StupidArtnetServer
from pyglet import app, clock, gl, image, window, shapes, graphics, canvas
from typing import List
from flask import Flask, request
from flask_socketio import SocketIO
import json

import chase

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
    t = get_bpm_time()
    with lock:
        rendered_layers.clear()

        for lid in layerids:
            l = layer.new()
            for pb in sorted(active_playbacks, key=lambda x: x["priority"]):
                playback.apply(pb, l, lid, t)

            playback.apply(programmer, l, lid, t)
        
            rendered_layers.append(l)

def update_playback_states():
    global active_playbacks, lock
    t = get_bpm_time()
    queue_on = []
    queue_off = []
    with lock:
        for pb in active_playbacks:
            pb_time = playback.get_playback_time(pb, t)
            if pb["chase"] != None:
                chaseTime = chase.get_chase_time(pb["chase"], pb_time)
                for chaseEntry in pb["chase"]["entries"]:
                    if chaseEntry["playback_id"] == None:
                        continue
                    if chaseEntry["start"] > pb["chase"]["lasttime"] and chaseEntry["start"] <= chaseTime:
                        queue_on.append(chaseEntry["playback_id"])
                    if chaseEntry["end"] > pb["chase"]["lasttime"] and chaseEntry["end"] <= chaseTime:
                        queue_off.append(chaseEntry["playback_id"])
                pb["chase"]["lasttime"] = chaseTime
            if pb["duration"] != 0 and t - pb["startbpmtime"] > pb["duration"]:
                if pb["chase"] != None:
                    for chaseEntry in pb["chase"]["entries"]:
                        queue_off.append(chaseEntry["playback_id"])
                queue_off.append(pb["id"])
    
    for onid in queue_on:
        on(pb_id = onid)

    for offid in queue_off:
        off(pb_id = offid)

def update_time(t):
    global realtime
    realtime = realtime + t

def update(t):
    update_time(t)
    update_playback_states()
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

    for l in rendered_layers:
        pygletshape = layer.get_shape(l, WIDTH, HEIGHT)
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
        pb["slot"] = request.json["slot"]
        pb["id"] = len(playbacks)
        playbacks.append(pb)
        apisocket.emit('new_playback', pb)
        return '', 200

@api.route('/api/playback/<pb_id>/meta', methods=["PATCH"])
def meta(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        for m in matches:
            print(request.json)
            if ("name" in request.json):
                m["name"] = request.json["name"]
            if ("key" in request.json):
                m["key"] = request.json["key"]
            if ("priority" in request.json):
                m["priority"] = request.json["priority"]
            if ("sync" in request.json):
                m["sync"] = request.json["sync"]
            if ("duration" in request.json):
                m["duration"] = request.json["duration"]
            apisocket.emit('update_playback', m)
        return '', 200

@api.route('/api/playback/<pb_id>/chase', methods=["POST"])
def chaseupdate(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        for m in matches:
            if m["chase"] == None:
                m["chase"] = chase.new_chase()
            m["chase"]["duration"] = request.json["duration"]
            apisocket.emit('update_playback', m)
        return '', 200
    
@api.route('/api/playback/<pb_id>/chase', methods=["DELETE"])
def chasedelete(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        for m in matches:
            m["chase"] = None
            apisocket.emit('update_playback', m)
        return '', 200
    
@api.route('/api/playback/<pb_id>/chase/entry', methods=["POST"])
def chase_entry_upsert(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        for m in matches:
            if m["chase"] == None:
                return '', 400
            entries = [x for x in m["chase"]["entries"] if x["id"] == request.json["id"]]
            pid = None
            if "playback_id" in request.json:
                pid = request.json["playback_id"]
            newentry = chase.ChaseEntry(start=request.json["start"], end=request.json["end"], playback_id=pid, id=request.json["id"])
            if len(entries) == 0:
                m["chase"]["entries"].append(newentry)
            else:
                for i, entry in enumerate(m["chase"]["entries"]):
                    if entry["id"] == newentry["id"]:
                        m["chase"]["entries"][i] = newentry
            apisocket.emit('update_playback', m)
    return '', 200

@api.route('/api/playback/<pb_id>/chase/entry/<entry_id>', methods=["DELETE"])
def chase_entry_delete(pb_id=0, entry_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    entry_id = int(entry_id)
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        for m in matches:
            if m["chase"] == None:
                return '', 400
            trimmedentries = [x for x in m["chase"]["entries"] if x["id"] != entry_id]
            m["chase"]["entries"] = trimmedentries
        apisocket.emit('update_playback', m)
    return '', 200

def on(pb_id=0):
    global playbacks, active_playbacks, lock
    pb_id = int(pb_id)
    t = get_bpm_time()
    with lock:
        matches = [x for x in playbacks if x["id"] == pb_id]
        for m in matches:
            m['startbpmtime'] = t
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
    
@display_window.event
def on_key_press(symbol, modifiers):
    if symbol == window.key.A:
        with lock:
            print(active_playbacks)
            print(playbacks)

def run_api():
    apisocket.run(api, port=4000)

if __name__ == "__main__":
    clock.schedule_interval(update, 1/120) # schedule 60 times per second
    apithread = threading.Thread(target=run_api)
    apithread.daemon = True
    apithread.start()
    app.run()


