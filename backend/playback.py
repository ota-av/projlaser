# A playback is a set of  

from layer import Layer
import param
from typing_extensions import TypedDict, Literal

AllowedParams = Literal["opacity", "hue", "saturation", "value", "x", "y", "sizex", "sizey", "rotation"]
AllowedTypes = Literal["rect", "tri", "star", "circ"]

class Playback(TypedDict):
    layervalues: dict[str, dict[AllowedParams, param.FxParam | AllowedTypes]]
    types: dict[str, str]
    id: int
    name: str
    priority: int
    key: Literal["flash", "toggle"]
    sync: bool
    startbpmtime: float | None
    duration: int

def apply(playback: Playback, layer: Layer, layerid: str, time: float):
    if not layerid in playback['layervalues']:
        return layer
    
    if (not playback["sync"] and "startbpmtime" in playback):
        time = time - playback["startbpmtime"]

    for prop in playback['layervalues'][layerid]:
        val = param.get(playback['layervalues'][layerid][prop], time)
        layer[prop] = val

    return layer

def new_playback(id):
    pb = Playback(layervalues={}, id=id, name="", priority=0, key="flash", sync=True, startbpmtime=None, duration=0)
    return pb

def setPlaybackValue(playback: Playback, layerid: str, param: AllowedParams, value: param.FxParam):
    if not layerid in playback['layervalues']:
        playback['layervalues'][layerid] = {}

    playback['layervalues'][layerid][param] = value
    return playback
