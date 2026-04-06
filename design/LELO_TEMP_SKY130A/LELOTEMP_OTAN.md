

Current mirror OTA. The bias is provided by the resistor from the tail of the
differential pair to VSS. With the CTAT voltage at the input the current should 
remain stable. I'm not using the bias current from the bandgap
because I don't want to complicate the loop startup behavior. 

The output of the OTA is pull high in power down to ensure that the PMOS current
mirror in the bandgap is turned off in power down.

The circuit on the right side is used to generate the cascode bias for the main
bandgap. 

The circuit on the far right is the startup circuit. The current from the
bandgap is fed to a very long PMOS. The VSTART1 voltage is buffered, and used to
pull down the VCP and VO voltage to get the loop started. If there is no current
flowing, then VSTART1 will be high. If there is some current then VSTART1 will
be low. 
