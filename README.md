
[![GDS](../../actions/workflows/gds.yaml/badge.svg)](../../actions/workflows/gds.yaml)
[![DRC](../../actions/workflows/drc.yaml/badge.svg)](../../actions/workflows/drc.yaml)
[![LVS](../../actions/workflows/lvs.yaml/badge.svg)](../../actions/workflows/lvs.yaml)
[![DOCS](../../actions/workflows/docs.yaml/badge.svg)](../../actions/workflows/docs.yaml)

# Who

Carsten Wulff

# Why

Example of a temperature sensor 

# How

See Schematic to see how it works

# What


| What          | Cell/Name                              |
|:--------------|:--------------------------------------:|
| Schematic     | design/LELO_TEMP_SKY130A/LELO_TEMP.sch |
| Layout        | design/LELO_TEMP_SKY130A/LELO_TEMP.mag |
| Verilog Model | design/LELO_TEMP_SKY130A/LELO_TEMP.v   |
| Verilog TB    | sim/tb_lelo_temp/tb.v                  |
| Analog top TB | sim/LELO_TEMP/tran.spi                 |


# Signal interface


| Signal       | Direction | Domain  | Description                                   |
|:-------------|:---------:|:-------:|:----------------------------------------------|
| VDD_1V8      | Input     | VDD_1V8 | Main supply                                   |
| PWRUP_1V8    | Input     | VDD_1V8 | Power up the temperature dependent oscillator |
| OSC_TEMP_1V8 | Output    | VDD_1V8 | Temperature dependent frequency               |
| VSS          | Input     | Ground  |                                               |

# Key parameters

| Parameter             | Min | Typ             | Max | Unit |
|:----------------------|:---:|:---------------:|:---:|:----:|
| Technology            |     | Skywater 130 nm |     |      |
| AVDD                  | 1.7 | 1.8             | 1.9 | V    |
| Oscillation frequency |     |                 |     |      |
| Temperature           | -40 | 27              | 125 | C    |




Typical temperature error 

![](sim/LELO_TEMP/tran_Sch_typical.png)

Mismatch

![](sim/LELO_TEMP/tran_Sch_mc.png)

Extreme test condition
![](sim/LELO_TEMP/tran_Sch_tec.png)
