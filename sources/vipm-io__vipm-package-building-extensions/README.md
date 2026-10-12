# VIPM Package Building Tools

This package contains some tools useful for package building with [VIPM Desktop](https://www.vipm.io/desktop/).

## Status

This tool is currently under development and is not yet available on vipm.io. If it works for you, you might want to copy the VIs and add them to your project or add it as a git submodule to your own project.

## Overview

This library is designed to be used in a post-build action in VIPM's package builder. It allows you to perform operations and package, right before it is finalized by the package builder.  It has tools for unpacking and repacking the package file, performing useful operations like what's shown below (in this case, setting a package's MNU file to synchronize with a specific directory) that are not directly supported by the high level VIPM Package Builder GUI.

![](https://user-images.githubusercontent.com/381432/141694191-8dcdeb11-3de0-4946-8299-26e8d1e1b8cc.png)

## Development

The source code for this package is developed (saved) in LV2020.
There is a .lvversion file that is used by newer LabVIEW versions to allow preseving sources code in LV2020 save format.