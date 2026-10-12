# LabVIEW Instrument Driver for Bronkhorst Mass Flow and Pressure Instruments with ProPar Protocol
Tested on Bronkhorst EL-FLOW.

## Requirements
LabVIEW 2015 and higher.

## Installation
[VIPM package](https://www.vipm.io/package/plasmapper_lib_pl_bronkhorst_propar/)

## Features
1. Low-level VIs to read/configure any device parameter.
2. High-level VIs to read/configure most used (in my opinion :)) parameters.
3. Automatic reconnection to device.

## Extra
[GCF Calculator Library](https://github.com/plasmapper/gcf-calculator-labview) can be used to calculate actual flow rate when using gas/mixture other than calibrated.

## Examples
### Bronkhorst ProPar.vi
Example VI that demonstrates library features.

### Controller Tuning.vi
Simple controller tuning VI.

## Documentation
[RS232 Interface with ProPar Protocol for Digital Multibus Mass Flow / Pressure Instruments](https://www.bronkhorst.com/getmedia/77a1438f-e547-4a79-95ad-53e81fd38a97/917027-Manual-RS232-interface.pdf)
