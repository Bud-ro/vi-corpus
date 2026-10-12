# NI VeriStand Scan Engine Module Libraries

The **NI VeriStand Scan Engine Module Libraries** provides built components to the [Scan Engine Custom Device](https://github.com/ni/niveristand-scan-engine-ethercat-custom-device) to support C Series and Remote I/O modules. Specifically, this repository contains the module UI and engine configuration code for all modules.

If installing the **Scan Engine Custom Device** from a [released package](https://github.com/ni/niveristand-scan-engine-ethercat-custom-device/releases/latest), you do not need to separately clone or install this component. Only modifications to the custom device's module support require using this repository as source. See the [documentation](https://github.com/ni/niveristand-scan-engine-ethercat-custom-device/blob/main/docs/Adding%20New%20Modules.md) found in the **Scan Engine Custom Device** repository for adding module support.

## LabVIEW Version

LabVIEW 2024

## Dependencies

- [NI CompactRIO](http://www.ni.com/en-us/support/downloads/drivers/download.ni-compactrio.html)
- [NI-Industrial Communications for EtherCAT](https://www.ni.com/en-us/support/downloads/drivers/download.ni-industrial-communications-for-ethercat.html)

## Git History & Rebasing Policy
Branch rebasing and other history modifications will be listed here, with several notable exceptions:
- Branches prefixed with `dev/` may be rebased, overwritten, or deleted at any time.
- Pull requests may be squashed on merge.

## License

The NI VeriStand Scan Engine Module Libraries are licensed under an MIT-style license (see LICENSE). Other incorporated projects may be licensed under different licenses. All licenses allow for non-commercial and commercial use.
