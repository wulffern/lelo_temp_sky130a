#!/usr/bin/env python3

import cicpy



def beforePlace(self):

    first_pmos = self.ckt.getInstances("xpb1<0>")[0]
    first_pmos.setProperty("xoffset",10)
    pass

def afterPlace(self):

    self.addRouteRing("M3","VS","b")
    self.addPowerRing("M1","VSS","b",1,6)
    self.addPowerRing("M1","VDD_1V8","t",4,6)

    pass

def beforeRoute(self):

    self.addRouteConnection("VS$","xpb","M2","bottom","")

    self.addPowerConnection("VDD_1V8","","bottom")
    self.addPowerConnection("VSS","","bottom")

    self.addConnectivityRoute("M2","VI(N|P)","||","",2,"","")

    pass
