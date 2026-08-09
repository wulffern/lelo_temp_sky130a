"""LELOTEMP_OTAR_XXFILL_P_SW_: this subcell's own layout hooks.

Generated once by `cicpy sch2subcells`, then yours: edit and commit.

Both hooks run in the parent, between its afterPlace and beforeRoute,
with `layout` the parent LayoutCell and `entry` this subcell's plan:
    entry["instances"]  the instance names in this subcell
    entry["ports"]      its boundary nets
    entry["internal"]   nets wholly inside it
    entry["type"]       stack | diffpair | mirror, from LELOTEMP.yaml
"""


def beforePlace(layout, entry):
    """Adjust this subcell's placement before anything routes."""


def beforeRoute(layout, entry):
    """Route this subcell's internal nets.

    Return True to claim the subcell as ROUTED -- the built-in stack
    router will then leave it alone. Return None to let the built-in
    router handle it, which is the right default.
    """
