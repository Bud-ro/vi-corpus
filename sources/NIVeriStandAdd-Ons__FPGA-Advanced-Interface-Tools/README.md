## FPGA Advanced Interface Tools ##

This Add-On is **deprecated** and is no longer updated with new features or bug fixes. Therefore, it is not recommended for use in new projects. A next-generation [FPGA Advanced Session Resources](https://decibel.ni.com/content/docs/DOC-35574) tool is available. The new tool offers vast improvements to API performance and features.

**FPGA Advanced Interface Tools** were created to provide a bitfile independent API layer to NI FPGAs.

### File Notes ###

Be careful about developing inside of user.lib because all the path linkings will point to user.lib and then relative from user.lib. Since the typedef class is a template and classes will be created from it that do not live in user.lib, the typedef template class must not be mass compiled within user.lib. The typedef class must also be linked to the base class that is located in user.lib so that all classes created from this template properly link to the base class located in user.lib.

The contents of "Source\_FPGA Interface Advanced Tools" are meant to be placed at "LabVIEW 2010\user.lib\_FPGA Interface Advanced Tools".
The contents of "Source\palette file" are meant to be placed at "LabVIEW 2010\menus\Categories\Addons\".
The contents of "Source\tools menu LLB" are meant to be placed at "LabVIEW 2010\project".

### LabVIEW Version ###

LabVIEW 2010

### Built Availability ###

Built version of this IP is available on the [NI Labs](https://decibel.ni.com/content/docs/DOC-17185)

### Quality, Limitations ###

This IP should be considered good quality and mature, but not as high of quality as the Advanced Session Resources which replaces it. This IP has been used worldwide by many customers in deployed applications since early 2010.

### License ###

*This repository and any materials provided by NI therein are provided AS IS. NI DISCLAIMS ANY AND ALL LIABILITIES FOR AND MAKES NO WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR  PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY. NI shall have no liability for any direct, indirect, incidental, punitive, special, or consequential damages for your use of the repository or any materials contained therein.*