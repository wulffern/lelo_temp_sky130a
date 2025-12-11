

Current mirror OTA. The bias is provided by the resistor from the tail of the
differential pair to VDD. I'm not using the bias current from the bandgap
because I don't want to complicate the loop startup behavior. 

The output of the OTA is pull high in power down to ensure that the PMOS current
mirror in the bandgap is turned off in power down.

