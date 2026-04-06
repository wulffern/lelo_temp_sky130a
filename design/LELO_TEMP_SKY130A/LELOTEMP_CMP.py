#!/usr/bin/env python3

#<<<<<<< HEAD
#import cicpy



#def beforePlace(self):

#    first_pmos = self.ckt.getInstances("xpb1<0>")[0]
#    first_pmos.setProperty("xoffset",10)
#    pass

#def afterPlace(self):

#    self.addRouteRing("M3","VS","b")
#    self.addPowerRing("M1","VSS","b",1,6)
#    self.addPowerRing("M1","VDD_1V8","t",4,6)

#    pass

#def beforeRoute(self):

#    self.addRouteConnection("VS$","xpb","M2","bottom","")

#    self.addPowerConnection("VDD_1V8","","bottom")
#    self.addPowerConnection("VSS","","bottom")

#    self.addConnectivityRoute("M2","VI(N|P)","||","",2,"","")

#    pass
#=======
data = {
    "afterPaint": [
        {"resetOrigins": [[1]]},
    ]
}


def _inst(layout, name):
    inst = layout.getInstanceFromInstanceName(name)
    if inst is None:
        raise ValueError(f"Missing instance {name}")
    return inst


def _restack(stack, ordered_names):
    insts = [inst for inst in stack.instances if getattr(inst, "instanceName", "") in ordered_names]
    if len(insts) != len(ordered_names):
        raise ValueError(f"Stack {stack.name} does not match requested order {ordered_names}")
    lookup = {inst.instanceName: inst for inst in insts}
    stack.instances = [lookup[name] for name in ordered_names]
    stack.stack(x=stack.left(), y=stack.bottom(), ygap=0)
    return stack


def beforePlace(layout):
    layout.noPowerRoute = True
    layout.place_xspace = [0]
    layout.place_yspace = [0]
    layout.place_groupbreak = [5]


def beforeRoute(layout):
    layout.addRouteRing("M1", "VDD_1V8", "t", widthmult=3, spacemult=2)
    layout.addRouteRing("M1", "VSS", "b", widthmult=3, spacemult=2)
    layout.addPowerConnection("VDD_1V8", "^xb", "top")
    layout.addPowerConnection("VSS", "^xa", "bottom")

    # All signal routes on M2 (M1 is reserved for power/taps/dummy-device routing)

    # Cross-domain routes (NMOS <-> PMOS, needs vertical component)
    #layout.addConnectivityRoute("M2", "^VBP2$", "-|--", "", 1, "", "")
    #layout.addConnectivityRoute("M2", "^net1$", "-|--", "", 1, "", "")
    #layout.addConnectivityRoute("M2", "^net2$", "-|--", "", 1, "", "")
    #layout.addConnectivityRoute("M2", "^VO$", "-|--", "", 1, "", "")

    # PMOS horizontal routes
    #layout.addConnectivityRoute("M2", "^VS$", "-", "", 1, "", "^xb")
    #layout.addConnectivityRoute("M2", "^PWRUP_1V8$", "-", "", 1, "", "^xb")
    #layout.addConnectivityRoute("M2", "^VIN$", "-", "", 1, "", "^xb")
    #layout.addConnectivityRoute("M2", "^VIP$", "-", "", 1, "", "^xb")

    # NMOS horizontal routes
    #layout.addConnectivityRoute("M2", "^IBP_1U$", "-", "", 1, "", "^xa")
    #layout.addConnectivityRoute("M2", "^PWRUP_N_1V8$", "-", "", 1, "", "^xa")


def afterPlace(layout):
    branch_gap = 2 * layout.um

    nmos = layout.makeCellGroup("nmos")
    n_bias_ref = nmos.addStack("n_bias_ref", [_inst(layout, "xaa_bias_ref<0>"), _inst(layout, "xaa_bias_ref<1>")])
    n_bias_mirror = nmos.addStack("n_bias_mirror", [_inst(layout, f"xab_bias_mirror<{i}>") for i in range(4)])
    n_left = nmos.addStack("n_left", [_inst(layout, "xac_left<0>"), _inst(layout, "xac_left<1>")])
    n_right = nmos.addStack("n_right", [_inst(layout, "xad_right<0>"), _inst(layout, "xad_right<1>")])
    n_out = nmos.addStack("n_out", [_inst(layout, "xae_out<0>")])

    pmos = layout.makeCellGroup("pmos")
    p_bias_ref = pmos.addStack("p_bias_ref", [_inst(layout, "xba_bias_ref<0>"), _inst(layout, "xba_bias_ref<1>")])
    p_bias_mirror = pmos.addStack("p_bias_mirror", [_inst(layout, f"xbb_bias_mirror<{i}>") for i in range(3)])
    p_left = pmos.addStack("p_left", [_inst(layout, "xbc_left<0>")])
    p_right = pmos.addStack("p_right", [_inst(layout, "xbd_right<0>")])
    p_out = pmos.addStack("p_out", [_inst(layout, "xbe_out<0>")])

    _restack(n_bias_ref, ["xaa_bias_ref<0>", "xaa_bias_ref<1>"])
    _restack(n_bias_mirror, [f"xab_bias_mirror<{i}>" for i in range(4)])
    _restack(n_left, ["xac_left<0>", "xac_left<1>"])
    _restack(n_right, ["xad_right<0>", "xad_right<1>"])
    _restack(n_out, ["xae_out<0>"])

    _restack(p_bias_ref, ["xba_bias_ref<1>", "xba_bias_ref<0>"])
    _restack(p_bias_mirror, ["xbb_bias_mirror<2>", "xbb_bias_mirror<1>", "xbb_bias_mirror<0>"])
    _restack(p_left, ["xbc_left<0>"])
    _restack(p_right, ["xbd_right<0>"])
    _restack(p_out, ["xbe_out<0>"])

    nmos.fillDummyTransistors(direction="top")
    n_bias_ref.addTaps()
    n_bias_mirror.addTaps()
    n_left.addTaps()
    n_right.addTaps()
    n_out.addTaps()

    pmos.fillDummyTransistors(direction="bottom")
    p_bias_ref.addTaps()
    p_bias_mirror.addTaps()
    p_left.addTaps()
    p_right.addTaps()
    p_out.addTaps()

    p_bias_ref.abutTop(n_bias_ref, space=branch_gap)
    p_bias_mirror.abutTop(n_bias_mirror, space=branch_gap)
    p_left.abutTop(n_left, space=branch_gap)
    p_right.abutTop(n_right, space=branch_gap)
    p_out.abutTop(n_out, space=branch_gap)
    pmos.updateBoundingRect()
    nmos.updateBoundingRect()
    nmos.routeDummyDevices()
    pmos.routeDummyDevices()
#>>>>>>> 79972615888c581bc1da283e39af7e167adf0aba
