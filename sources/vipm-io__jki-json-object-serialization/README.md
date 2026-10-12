# JKI JSON Object Serialization

![image](https://github.com/JKISoftware/JKI-JSON-Object-Serialization/assets/381432/c2b9f1a4-3813-4c1a-84ae-ab18b6df4b66)

[![CI](https://github.com/JKISoftware/JKI-JSON-Object-Serialization/actions/workflows/ci.yml/badge.svg)](https://github.com/JKISoftware/JKI-JSON-Object-Serialization/actions/workflows/ci.yml)
[![Image](https://www.vipm.io/package/gcraftsman_lib_json_object_serialization/badge.svg?metric=installs)](https://www.vipm.io/package/gcraftsman_lib_json_object_serialization/)
[![Image](https://www.vipm.io/package/gcraftsman_lib_json_object_serialization/badge.svg?metric=stars)](https://www.vipm.io/package/gcraftsman_lib_json_object_serialization/)

Note: This library has not been actively maintained and is undergoing upgrades. Please stay tuned.

The JKI JSON Object Serialization is an extension of the popular JKI JSON Library.  It was originally created by Michael Lacasse at GCraftsman and open sourced in 2022 so that JKI and the community could maintain and evolve it.

It provides the additional feature of serializing and de-serializing LabVIEW Class Objects to/from JSON.  It was inspired and modeled after widely-adopted serializers like GSON and Jackson, to facilitate interoperability with applications developed in other languages.
Powerful features include:

- De-serialization handles out-of-order and missing or extra items. Class hierarchical relationships and composition are treated as nested clusters. Objects can be de-serialized to ancestor types yet retain child data. Accessor methods to class private data are not required!

This code library is a valuable tool to help simplify and short-cut the development process of  messaging architectures or configuration file handling.  Use it to quickly develop flexible solutions, free of custom-conversion "glue" code that tends to be fragile and require frequent maintenance to support new data types and backward compatibility.

Performs best-fit de-serialization to convert JSON to LabVIEW object, cleanly handling out-of-order and missing or extra items.

Class hierarchical relationships and composition are treated as nested clusters.
Objects can be de-serialized to any ancestor type (including LabVIEW Object), and still retain child data.

This library depends on these other packages:
JKI JSON >= 1.1.10.37
