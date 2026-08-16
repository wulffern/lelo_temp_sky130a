# tt_um_lelo_temp_wulffern — function simulation

Does the tile work **through the TinyTapeout pins**: power arrives on
VDPWR, PWRUP_ANA rises on `ui_in[0]`, and the oscillator must appear on
`uo_out[0]`. This bench owns only what the wrapper adds — the pad
routing, the tie-low resistors, the antenna diode, the strapped rings
and the wide power stacks. The exhaustive corner work lives with
`sim/LELO_TEMP`.

Run both views:

    make both        # = make typical VIEW=Sch ; make typical VIEW=Lay

## Result (Gt Ktt Tt Vt, 2026-08-16)

| measure | view | -40 C | 25 C | 125 C |
|---|---|---|---|---|
| f_OSC on uo_out[0] | Sch | 1.70 MHz | 2.42 MHz | see .logm |
|                    | Lay | 1.40 MHz | 1.99 MHz | see .logm |
| idd (running)      | Sch | 61 uA | 84 uA | |
|                    | Lay | 61 uA | 83 uA | |
| iddq (powered down)| Sch | 4.3 nA | 7.1 nA | |
|                    | Lay | 5.5 nA | 11 nA | |
| uio_oe[0], uio_oe[7] | both | 0 V | 0 V | |

Frequency = 4/(t2 − t1), edges 1..5 of `uo_out[0]` after PWRUP.
The ~18 % Lay slowdown is the full-RC extraction.

## Three traps this bench stepped in (kept working, in the files)

* xschem netlists the tree with `<>` buses; the TT ports are `[]` in
  the DEF. The netlist step maps only the five TT prefixes to `[]`
  (magic's own extraction spells them `<>` again, but SPICE binds
  subckt pins by position, so one `[]`-named bench serves both views).
* the LPE netlist never meets `fixsubckt`, so the antenna diode went to
  the simulator with magic's units — area 2.025e11 square METRES — and
  the solver died at the first movement of `ui_in[0]`, every
  temperature. The netlist step converts to SI, idempotently.
* a 10 ps PWRUP edge is unsimulatable against full RC and unphysical
  from a pin mux; the bench uses 10 ns.
