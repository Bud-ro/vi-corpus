## CAN Log Service and Converter ##

**CAN Log Service and Converter** is source for a stand alone exe and NI VeriStand service whose primary goal is to convert CAN log files (*.ncl) to human readable text and retrieve them from the target automatically. The user can select if they want the NCL file converted to text in the "NI-CAN" style of text log, or the "NI-XNET" style of text log. 

The service, when added to an NI VeriStand project, associates raw CAN logs saved on the execution target with legacy stimulus profiles. The service runs whenever you connect the host system to the NI VeriStand engine. As a legacy stimulus profiles complete, it identifies which raw CAN logs on the target are associated with each legacy stimulus profile. This information is stored in a queue for processing later so that the target is not disturbed while running the legacy stimulus profiles. If the user selects the dialog and presses "Fetch CAN logs" OR disconnects the host from the NI VeriStand engine, the CAN logs are FTP'd off the target and placed into the associated logging directory for that stimulus profile on the host. Additionally, it converts the binary (.ncl) files to text files.

To use the service:

1. Add this service to your NIVS project
2. Edit your system definition file to contain a conditional calculated channel. Pick channel to check as GEN001 State. Configure the if true case to output 1, and if false case to output 0. This calculated channel will be used to trigger the raw CAN logging based upon generator 1 state. Therefore, raw CAN logging will only happen during stimulus profiles. 
3. Add/edit your raw can logging trigger configuration to be "Enable logging when trigger value is not zero".
4. Edit your raw can logging trigger to be your calculated channel.
5. Save and close your sysdef
6. FTP in to your target Ftp://<ipaddress>/ni-rt/NIVeriStand/XNET/Raw Data Logs/ and copy off any old logs there you want to save.
7. Deploy and connect. Now as you run batch/sequence stimulus profiles, the raw data logs will be in the appropriate logs directory.

This service makes several assumptions:

1. The raw data logs directory on the target does not contain any logs you wish to keep before the very first use of this service
2. You always run stimulus profiles with the batch/sequence editor.

**IMPORTANT WARNINGs:**

1. For proper operation, this service requires the Raw Data Logs folder on the target be empty when it starts, therefore it will delete all the logs out of there when it starts. Make sure you get everything out of that folder before using this the first time.
2. Wait for the FTP transfer to finish before reconnecting the host to the target.

### LabVIEW Version ###

LabVIEW 2010

### Built Availability ###

No builds are provided.

### Quality, Limitations ###

This IP was developed for a specific use case in 2010 and has not been tested since. It has not been updated for either the new CAN log format (*.tdms) or new NI VeriStand stimulus profiles. Therefore, this has some usefulness for legacy project but needs upgrades to be useful for new projects.

### License ###

*This repository and any materials provided by NI therein are provided AS IS. NI DISCLAIMS ANY AND ALL LIABILITIES FOR AND MAKES NO WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR  PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY. NI shall have no liability for any direct, indirect, incidental, punitive, special, or consequential damages for your use of the repository or any materials contained therein.*