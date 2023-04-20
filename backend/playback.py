# A playback is a set of  

from layer import FxParam, Layer
from typing_extensions import TypedDict

# A single value for a layer
class PlaybackValue(TypedDict):
    property: str
    value: FxParam


class Playback(TypedDict):
    layervalues: dict[str, list[PlaybackValue]]
    id: str
    name: str


def apply(playback: Playback, layer: Layer, layerid: str):
    if not layerid in playback['layervalues']:
        return layer

    for pval in playback['layervalues'][layerid]:
        layer[pval['property']] = pval['value']

    return layer
