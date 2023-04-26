from typing_extensions import TypedDict

from math import fmod

class ChaseEntry(TypedDict):
    start: float
    end: float
    playback_id: int
    id: int

class Chase(TypedDict):
    duration: float
    entries: list[ChaseEntry]
    lasttime: float

def new_chase():
    return Chase(duration=1, entries=[])

def get_chase_time(chase: Chase, playbacktime: float): # time is playbacktime
    return fmod(chase['duration'] - playbacktime, chase['duration'])