from shape import Shape, FxParam
defaultRect = Shape()
defaultRect.type = "rect"
defaultRect.sizex = FxParam(1)
defaultRect.sizey = FxParam(0.1)

rectUpdown = Shape()
rectUpdown.type = "rect"
rectUpdown.sizex = FxParam(1)
rectUpdown.sizey = FxParam(0.25)
rectUpdown.y = FxParam(0.7, "sine", 0.2, 1)


blackmid = Shape()
blackmid.type = "circ"
blackmid.v = FxParam(0)
blackmid.sizex = FxParam(0.3)


rectLeft = Shape()
rectLeft.type = "rect"
rectLeft.x = FxParam(0.25)
rectLeft.sizex = FxParam(0.5)
rectLeft.sizey = FxParam(1)
rectLeft.s = FxParam(0)

rectRight = Shape()
rectRight.type = "rect"
rectRight.x = FxParam(0.75)
rectRight.sizex = FxParam(0.5)
rectRight.sizey = FxParam(1)
rectRight.s = FxParam(0)

rotStar = Shape()
rotStar.type = "star"
rotStar.r = FxParam(0, "linear", 1, 1, 0)

rotatingLine = Shape()
rotatingLine.type = "rect"
rotatingLine.r = FxParam(0, "linear", 1, 0.75, 0)
rotatingLine.sizex = FxParam(1)
rotatingLine.sizey = FxParam(0.15)
rotatingLine.s = FxParam(0)

rotatingLineOffset = Shape()
rotatingLineOffset.type = "rect"
rotatingLineOffset.r = FxParam(0, "linear", 1, 0.75, 0.25)
rotatingLineOffset.sizex = FxParam(1)
rotatingLineOffset.sizey = FxParam(0.15)
rotatingLineOffset.s = FxParam(0)