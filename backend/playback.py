# A playback is a set of  

from layer import Layer
import param
from typing_extensions import TypedDict, Literal
from chase import Chase

AllowedParams = Literal["opacity", "hue", "saturation", "value", "x", "y", "sizex", "sizey", "rotation", "type"]
AllowedTypes = Literal["rect", "tri", "star", "circ"]

class Playback(TypedDict):
    layervalues: dict[str, dict[AllowedParams, param.FxParam | AllowedTypes]]
    chase: Chase | None
    id: int
    name: str
    priority: int
    key: Literal["flash", "toggle"]
    sync: bool
    startbpmtime: float | None
    duration: float
    link_multiplier_id: str | None

def apply(playback: Playback, layer: Layer, layerid: str, bpmtime: float, multipliers: dict[str, float]):
    if not layerid in playback['layervalues']:
        return layer
    
    bpmtime = get_playback_time(playback, bpmtime, multipliers)
    
    for prop in playback['layervalues'][layerid]:
        if prop == 'type':
            layer[prop] = playback['layervalues'][layerid][prop]
        else:
            val = param.get(playback['layervalues'][layerid][prop], bpmtime)
            layer[prop] = val

    return layer

def get_playback_time(playback: Playback, bpmtime: float, multipliers: dict[str, float]):
    if (not playback["sync"] and "startbpmtime" in playback):
        bpmtime = bpmtime - playback["startbpmtime"]
    if playback['link_multiplier_id'] != None and playback["link_multiplier_id"] in multipliers:
        return bpmtime * multipliers[playback["link_multiplier_id"]]
    return bpmtime

def new_playback(id):
    pb = Playback(layervalues={}, id=id, name="", priority=0, key="flash", sync=True, startbpmtime=None, duration=0, chase=None, link_multiplier_id=None)
    return pb

def setPlaybackValue(playback: Playback, layerid: str, param: AllowedParams, value: param.FxParam):
    if not layerid in playback['layervalues']:
        playback['layervalues'][layerid] = {}

    playback['layervalues'][layerid][param] = value
    return playback
