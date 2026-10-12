**NOTICE: This repository has been archived, and will no longer be maintained or accept pull requests.**

## GE Reflective Memory Custom Device ##

**GE Reflective Memory Custom Device** is actually called the "RefMem PtByPt Custom Device" in code. **It is only useful for interfacing with 3rd party systems, as NI VeriStand's built in GE RefMem support is vastly superior for communicating between NI VeriStand targets**. It was originally developed to work around the fact that NI VeriStand 2010's GE reflective memory support always read/write in blocks, which had terrible performance if the addresses being written were scattered throughout the memory map. Therefore, this custom device reads and writes each address one call at a time. 

NI VeriStand 2011 and later also do this, so the main value of this custom device is gone. However, this custom device does support decimation, parallel (non-inlined) operation, and config file import/export- which NI VeriStand does not, so there is still some value.

### API ###

The LabVIEW project also contains code for a corresponding system definition API, and a build into a packed library.

The System Definition API allows configuring the Red RefMem PtByPt Custom device without using the system explorer. Use these API calls in tandem with the .NET NI VeriStand System Definition API. There is an example LLB provided with 3 top level examples.

### LabVIEW Version ###

LabVIEW 2010

### Built Availability ###

No builds are available.

### Quality, Limitations ###

This IP should be considered high quality and mature. The IP was developed for one specific customer in 2010 and was deployed successfully. No other users are known. 

### License ###

*This repository and any materials provided by NI therein are provided AS IS. NI DISCLAIMS ANY AND ALL LIABILITIES FOR AND MAKES NO WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR  PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY. NI shall have no liability for any direct, indirect, incidental, punitive, special, or consequential damages for your use of the repository or any materials contained therein.*
