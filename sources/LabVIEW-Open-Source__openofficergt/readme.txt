Open Office RGT addon v0.2.0 beta

Copyright © 2010-2016, François Normandin.
All rights reserved.


Author:François Normandin
Contact Info: Contact via PM on www.lavag.org

LabVIEW Versions:
Created and tested with LabVIEW 2009

Dependencies:
Report Generation toolkit (part of it is included in the base package: Word & Excel require license)


Description:
This package contains an installer and class to use the AODL (An OpenDocument library) with the Report Generation toolkit
from National Instruments.

Includes:

- ooWriter class
- AODL classes (and DLLs)
- PreInstall and PreUninstall VIs to backup the only modified NI VI: New Report.vi (in Utility\NIReport.llb)


Instructions:
After installing package with VIPM, use the NI Report Generation palette as usual.


Known Issues:

1- ooWriter: 
Styles integration is incomplete. Needs to have a real "style" class created that will comply with current standard in RGT.
Adding an image is not working correctly: it is embedded in a paragraph instead of being standalone.

2- ooCalc: no integration yet, but rather similar to ooWriter in principle. (All the roadblocks will be cleared by ooWriter)

3- This code has been done with LV2009. I see no problem for using with LV 8.2 and up, it's just a matter of 
saving for previous version and distribute. This will be done at a later date.


Acknowledgements:
National Instruments. (NI Report Generation Toolkit) ** LVOOP rocks **
AODL by Sun Microsystems, Inc. Copyright 2007
         
      
History:

v0.2.0: released on bitbucket (Git) for community

v0.1.0: Initial release of the code. (LV2009)



License:

LabVIEW libraries of OpenOffice for RGT addon are licensed under BSD.
AODL us distributed under the LGPL license.
(see license files for more detail)


Support:
If you have any problems with this code or want to suggest features:
please go to www.lavag.org and Navigate to the discussion page.

Distribution:
This code was downloaded from the LAVA Code Repository found at www.lavag.org 

============================

