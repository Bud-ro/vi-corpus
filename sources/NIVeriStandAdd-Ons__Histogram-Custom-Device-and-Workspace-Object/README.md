## Histogram Custom Device & Workspace Object ##

The **Histogram Custom Device & Workspace Object** allow you to analyze your data into bins on the target, then display this data as a histogram on your workspace.

### LabVIEW Version ###

The custom device and workspace object were created in LabVIEW 2012.

### Built Availability ###

Built versions of this device are not available. Download the source and build it to use this device.

### Quality, Limitations ###

This code was created as a proof of concept. It is of good quality and is functional, but has not been extensively tested on various targets and configurations.

The code currently only monitors/handles 1 channel per custom device and workspace object. Functionality could be added to display multiple channel histograms on the same graph if desired.

### Dependencies ###

The workspace object can only be used in conjunction with this custom device since it is expecting certain properties associated with the device. I.E. you cannot use the histogram object with just any channels in your system definition file. However, you can easily add the custom device and set it to monitor your channel(s).

### License ###

*This repository and any materials provided by NI therein are provided AS IS. NI DISCLAIMS ANY AND ALL LIABILITIES FOR AND MAKES NO WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR  PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY. NI shall have no liability for any direct, indirect, incidental, punitive, special, or consequential damages for your use of the repository or any materials contained therein.*