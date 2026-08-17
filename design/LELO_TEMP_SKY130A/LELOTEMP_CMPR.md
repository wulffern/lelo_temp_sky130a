A two-stage OTA used as comparator. Uses a 1U bias current from the bandgap.
Same circuit idea as LELOTEMP\_CMP, rebuilt from the REY\_ATR library.

It also owns the ramp node housekeeping: an NMOS gated by RST discharges the
integrating node between cycles, and one gated by PWRUP\_N holds it down in
power down.
