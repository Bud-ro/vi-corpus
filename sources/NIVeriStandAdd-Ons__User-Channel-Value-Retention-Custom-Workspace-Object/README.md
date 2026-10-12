## Deprecated!!##

This add-on has been deprecated. The Channel Value Retention Service (https://github.com/NIVeriStandAdd-Ons/Channel-Value-Retention-Service) is recommended for new systems.

## User Channel Value Retention Custom Workspace Object ##

The are scenarios in which it can be necessary to retain system values across an un-deploy and re-deploy of the System Definition file. For example, lets say you're using a user channel to count the test cycles of an ECU and you're incrementing this value. Sometime through your test, you realize you need to un-deploy the system to change an alarm value. So, you un-deploy, make your changes, and redeploy. But your user channels (and all others for that matter) will return to their default values and we're running a long-term test so we want to continue counting cycles from where we left off. This workspace tool allows your User Channels to be re-deployed with the value they had when the system was un-deployed (assuming the workspace was open). The workspace object monitors user selected User Channels and sets their default values in the host side copy of the System Definition file so when the system is redeployed it uses these new values.   

### LabVIEW Version ###

This Add-On was developed using LabVIEW 2012

### Built Availability ###

There are no available builds of this IP.

### Quality, Limitations ###

This IP has two known issues:

1. The workspace object must be running in order to properly track your User Channels. Unfortunately, only the first screen of the Workspace is started when the workspace is first opened. So, this Workspace Object either needs to be placed on your first Workspace screen or you need to ensure that you go to the screen that contains this object every time you deploy your System Definition file, to start that screen and thereby this object. This is a limitation of VeriStand, not this add-on.

2. Based on how the channels are being queried, the System Definition file must be deployed before you can configure the workspace object. The workspace object source could be modified to poll the channels when the system is offline or undeployed. 

### Dependencies ###

Simple System Definition API (https://decibel.ni.com/content/docs/DOC-26812)

### License ###

*This repository and any materials provided by NI therein are provided AS IS. NI DISCLAIMS ANY AND ALL LIABILITIES FOR AND MAKES NO WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR  PARTICULAR PURPOSE, OR NON-INFRINGEMENT OF INTELLECTUAL PROPERTY. NI shall have no liability for any direct, indirect, incidental, punitive, special, or consequential damages for your use of the repository or any materials contained therein.*