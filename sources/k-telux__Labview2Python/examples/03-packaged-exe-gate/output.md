# Reference Output

## Packaging Diagnosis

An early one-file build launched its bootloader and created an unpack directory
but never reached Python entry or the main window. The packaging spec used broad
framework collection that made the executable oversized and startup unreliable.
Relying on native PyInstaller hooks plus only required hidden imports produced a
cleaner current-source build.

## Accepted Build Evidence

- root/dist SHA256 identity;
- build time after relevant source and verifier mtimes;
- shortcut target, arguments, working directory, icon, and GUI subsystem;
- explicit runtime markers for Python entry and main-window readiness.

## Remaining Gate

Build success is not `packaged_exe_verified`. The status remains partial until
the exact distributable and shortcuts complete the required UI scenarios and
saved-output readback. Real hardware remains `unvalidated_blocked`.
