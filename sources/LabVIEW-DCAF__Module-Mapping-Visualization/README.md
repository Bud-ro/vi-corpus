Module-Mapping-Visualization
============================

This code uses GraphViz to take an engine configuration and generate a graphical representation of its modules and mappings.

Setup Instructions:
1. Install GraphViz  http://www.graphviz.org/Download.php
2. Add 'C:\Program Files (x86)\GraphvizX.XX\bin' to you OS path variable.  This is necessary for the command line integration to work.
3. Call 'GraphViz Generator UI Wrapper.vi' with the Engine Configuration and array of Module Configurations that you would like to visualize.

A great way to use this tool is to integrate it with the mappings editor node of the engine you are using.  This can be done easily by adding a new button, creating an event to handle that button press, and calling 'GraphViz Generator UI Wrapper.vi' in the event case with that engine's data. 
