import math
from typing_extensions import TypedDict, Literal

FxFuncMap = {
    "static": lambda x : 0,
    "flash": lambda x: 1 if (x > 0 and x < 1) else 0,
    "cos": lambda x: math.cos(x*2*math.pi),
    "sine": lambda x: math.sin(x*2*math.pi),
    "linear": lambda x: x,
    "square": lambda x: x*x,
    "cubic": lambda x: x*x*x,
    "sqrt": lambda x: x**0.5,
    "cbrt": lambda x: x**(1/3),
}

FxFuncs = Literal["static", "static_on", "sine", "linear", "flash", "square", "cubic", "cos", "sqrt", "cbrt"]

class FxParam(TypedDict):
    value: float
    func: FxFuncs
    phase: float
    speed: float
    scale: float
    start: float
    end: float
    

def get(param: FxParam, time):
    beattime = (time*param["speed"] + param["phase"]) % 1

    fxtime = beattime - param["start"]
    if(abs(param["end"] - param["start"]) > 0.001):
        fxtime = (beattime - param["start"])/(param["end"]-param["start"])
    

    if(fxtime) < 0:
        fxtime = 0
    if(fxtime) > 1:
        fxtime = 1
    return param["value"] + FxFuncMap[param["func"]](fxtime)*param["scale"]

def new(initial: float = 0, func: FxFuncs = "static", speed: float = 1, scale: float = 1, phase: float = 0):
    return FxParam(value=initial, func=func, phase=phase, speed=speed, scale=scale, start=0, end=1)
