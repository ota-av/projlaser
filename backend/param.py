import math
from typing_extensions import TypedDict, Literal

FxFuncMap = {
    "static": lambda x : 0,
    "sine": lambda x: math.sin(x*2*math.pi),
    "linear": lambda x: x,
    "flash": lambda x: 1 if (x < 0.5) else 0
}

FxFuncs = Literal["static", "sine", "linear", "flash"]

class FxParam(TypedDict):
    value: float
    func: FxFuncs
    phase: float
    speed: float
    scale: float
    

def get(param: FxParam, time):
    return param["value"] + FxFuncMap[param["func"]]((time*param["speed"] + param["phase"]) % 1)*param["speed"]

def new(initial: float = 0.5, func: FxFuncs = "static", speed: float = 1, scale: float = 1, phase: float = 0):
    return FxParam(value=initial, func=func, phase=phase, speed=speed, scale=scale)
