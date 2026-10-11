## Channel Value Retention Service ##

This service allows you to programmatically poll user-selected channels periodically throughout deployment and set the last values of those channels as default values. Ultimately, this will allow long-term tests to be run despite un-deployments and re-deployments and allow the system to resume in a similar state as it was in at the time it was un-deployed.

A new .ini file for the service is created for each system definition and is saved at the same level in the VeriStand project. This .ini file will allow you to configure the periodic polling rate (default is 10 Hz or 100 ms), the visibility of the service, and the default channels to monitor. At the end of each deployment, the current values monitored by the service will be saved as the default channels to monitor in the .ini file.


### LabVIEW Version ###

This service was developed using LabVIEW 2015 SP1.

### Built Availability ###

There are no available builds of this IP.

### Quality, Limitations ###

IP has been tested by developer.

The channel value update rate is limited by the VeriStand Gateway update rate of 15 Hz. Therefore, there is some latency in the channel value update rate which could cause a loss of data between the last update and the time of undeployment. 

### Dependencies ###

NI VeriStand 2015

### License ###

*This repository and any materials provided by NI therein are provided AS IS. NI DISCLAIMS ANY AND ALL LIABILITIES FOR AND MAKES NO WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR  PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY. NI shall have no liability for any direct, indirect, incidental, punitive, special, or consequential damages for your use of the repository or any materials contained therein.*