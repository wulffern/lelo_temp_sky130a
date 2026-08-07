"""cicpy layout hooks for LELOTEMP_CASCBIAS.

Uncomment the hooks you need. Each hook receives the LayoutCell object
as ``layout``.
"""


# def beforePlace(layout):
#     pass


def afterPlace(layout):
    nmos = layout.makeCellGroup("nmos")
    n_vbnt = nmos.addStackByGroup("xn_vbnt").stack().addTaps()
    n_vcn = nmos.addStackByGroup("xn_vcn").stack().addTaps()
    n_cap = nmos.addStackByGroup("xn_cap").stack().addTaps()

    pmos = layout.makeCellGroup("pmos")
    p_mirr = pmos.addStackByGroup("xp_mirr").stack().addTaps()
    p_vcp = pmos.addStackByGroup("xp_vcp").stack().addTaps().abutRight(p_mirr)
    p_src = pmos.addStackByGroup("xp_src").stack().addTaps().abutRight(p_vcp)

    pmos.abutRight(nmos,space=2*layout.um)

    pass


# def beforeRoute(layout):
#     pass


# def afterRoute(layout):
#     pass


# def beforePaint(layout):
#     pass


# def afterPaint(layout):
#     pass


# def beforePorts(layout):
#     pass


# def afterPorts(layout):
#     pass
