from layer import Layer, FxParam
defaultRect = Layer()
defaultRect.type = "rect"
defaultRect.sizex = FxParam(1)
defaultRect.sizey = FxParam(0.1)

rectUpdown = Layer()
rectUpdown.type = "rect"
rectUpdown.sizex = FxParam(1)
rectUpdown.sizey = FxParam(0.25)
rectUpdown.y = FxParam(0.7, "sine", 0.2, 1)


blackmid = Layer()
blackmid.type = "circ"
blackmid.value = FxParam(0)
blackmid.sizex = FxParam(0.3)


rectLeft = Layer()
rectLeft.type = "rect"
rectLeft.x = FxParam(0.25)
rectLeft.sizex = FxParam(0.5)
rectLeft.sizey = FxParam(1)
rectLeft.saturation = FxParam(0)

rectRight = Layer()
rectRight.type = "rect"
rectRight.x = FxParam(0.75)
rectRight.sizex = FxParam(0.5)
rectRight.sizey = FxParam(1)
rectRight.saturation = FxParam(0)

rotStar = Layer()
rotStar.type = "star"
rotStar.rotation = FxParam(0, "linear", 1, 1, 0)

rotatingLine = Layer()
rotatingLine.type = "rect"
rotatingLine.rotation = FxParam(0, "linear", 1, 0.75, 0)
rotatingLine.sizex = FxParam(1)
rotatingLine.sizey = FxParam(0.15)
rotatingLine.saturation = FxParam(0)

rotatingLineOffset = Layer()
rotatingLineOffset.type = "rect"
rotatingLineOffset.rotation = FxParam(0, "linear", 1, 0.75, 0.25)
rotatingLineOffset.sizex = FxParam(1)
rotatingLineOffset.sizey = FxParam(0.15)
rotatingLineOffset.saturation = FxParam(0)