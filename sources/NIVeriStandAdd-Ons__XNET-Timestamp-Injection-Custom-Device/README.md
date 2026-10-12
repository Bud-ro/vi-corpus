## XNET Timestamp Injection Custom Device ##

The **XNET Timestamp Injection Custom Device** was made as a proof of concept to demonstrate injecting timestamps into XNET raw logs onto multiple ports, configured at different baud rates, using a PXI trigger line. 

It is common for test systems to have multiple CAN ports, and to want the raw logs from these ports to be time aligned. Since ports on the XNET cards are not automatically time aligned, this has to be done in post processing. In applications with multiple ports on the same bus, this can be done by injecting a common frame onto the bus and aligning all logs on that timestamp. For applications with ports on different buses, however, this "common" frame used for time alignment must be injected via a trigger line. XNET allows for timestamp injection using a PXI trigger line. 

This code was developed specifically for PXI and injects a timestamp into the configured ports' logs when PXI_Trig4 goes high. 

### LabVIEW Version ###

This code was originally developed in LabVIEW 2013.

### Built Availability ###

Built versions of this device are not available. Download the source and build it to use this device.

### Quality, Limitations ###

This code was created as a proof of concept, and has not been thoroughly tested on varying hardware configurations. This code was also only tested on PXI, it has not been tested or designed for use on other platforms. 

### Dependencies ###

This custom device requires NI-XNET.

### License ###

*This repository and any materials provided by NI therein are provided AS IS. NI DISCLAIMS ANY AND ALL LIABILITIES FOR AND MAKES NO WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR  PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY. NI shall have no liability for any direct, indirect, incidental, punitive, special, or consequential damages for your use of the repository or any materials contained therein.*