data = {
    "afterPaint": [
        {"resetOrigins": [[1]]},
    ]
}


def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [6]




def afterPlace(layout):
    um = layout.um
    branch_gap = 2 * um
    macro_gap = 4 * um


def beforeRoute(layout):
    #layout.addRouteRing("M3", "VDD_1V8", "t", widthmult=3, spacemult=2)
    #layout.addRouteRing("M3", "VSS", "b", widthmult=3, spacemult=2)
    #layout.addPowerConnection("VDD_1V8", "", "top")
    #layout.addPowerConnection("VSS", "", "bottom")
    pass

def afterPorts(layout):
    pass
    #layout.addPortOnEdge("M4", "VO", "top", "||", "track10")
    #layout.addPortOnEdge("M4", "VCP", "top", "||", "track6")
    #layout.addPortOnEdge("M2", "VIN", "bottom", "||", "track2")
