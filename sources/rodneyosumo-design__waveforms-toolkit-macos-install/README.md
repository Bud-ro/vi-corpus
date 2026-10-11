# Installing the Digilent WaveForms Toolkit for LabVIEW on macOS

A working method for getting the **Digilent WaveForms Toolkit for LabVIEW** (the `DigilentWF`
VIs) running on **macOS**, where the official package is **Windows-only**.

If you opened a LabVIEW project that drives a Digilent **Analog Discovery** (2 / 3 / Pro /
**Studio** / **Studio Max**) instrument on a Mac and got *missing-VI / "LabVIEW Tools Network
add-on not installed" / broken run-arrow* errors, this is for you.

> ⚠️ **Unofficial workaround.** The toolkit's VIPM package is flagged `Exclusive_OS="Windows x64"`,
> and VI Package Manager isn't supported on macOS. This guide hand-installs the VIs that VIPM
> would normally place, and links the WaveForms native library so LabVIEW can find it. It works,
> but it is not a sanctioned install — see [Caveats](#8-known-caveats--maintenance). The reliable
> alternative is to run the project on **Windows**, where the toolkit installs normally via VIPM.

---

## TL;DR

```bash
# 1. Install the WaveForms app (provides the native dwf library + runtime/Adept):
#    https://digilent.com/shop/software/digilent-waveforms/download
# 2. Download the toolkit .vip from https://www.vipm.io/package/digilent_waveforms_vis/
# 3. Run the install script (see install_digilentwf_mac.sh in this repo):
sudo bash install_digilentwf_mac.sh
# 4. Open your .lvproj in LabVIEW and run it.
```

---

## 1. Symptoms

- Opening the `.lvproj` / main `.vi` produces errors and the VI won't run (broken run arrow,
  "subVI not found" / missing-VI errors).
- The reported cause is a missing **"LabVIEW Tools Network add-on."**

## 2. Why it happens

LabVIEW talks to the Analog Discovery hardware through a layered stack:

```
LabVIEW program (your project)        <- what you're trying to run
        | calls
WaveForms LabVIEW VIs (DigilentWF)    <- THE COMMONLY MISSING PIECE (the driver/bridge)
        | calls
WaveForms SDK / dwf native library    <- ships inside WaveForms.app
        | drives
Digilent Analog Discovery hardware
```

Installing the **WaveForms app** gives you the *engine* (the `dwf` library + runtime), but **not**
the *LabVIEW-to-engine bridge* (`DigilentWF` VIs). Without that bridge, every hardware call in the
project resolves to a missing VI. On Windows you'd add the bridge with VIPM; on macOS you can't, so
you install it by hand.

## 3. Prerequisites

| Requirement | Notes |
|-------------|-------|
| LabVIEW for macOS | The toolkit needs **LabVIEW ≥ 2021**. Examples below use **LabVIEW 2026 64-bit**. |
| WaveForms app | Install from Digilent. Provides the native `dwf` library and the **Adept Runtime**. |
| The toolkit `.vip` | `digilent_waveforms_vis-*.vip` from <https://www.vipm.io/package/digilent_waveforms_vis/> (a `.vip` is just a ZIP). |

## 4. Diagnose your own setup (optional)

```bash
# Is the DigilentWF add-on already in LabVIEW's vi.lib? (no output = missing)
find "/Applications/National Instruments/LabVIEW 2026 64-bit" -type d -iname DigilentWF

# Is the WaveForms app installed, and where is its native framework?
ls -d /Applications/WaveForms.app
find /Applications/WaveForms.app -iname "*dwf*"

# Is the native library linked to the standard SDK location? (often missing)
ls -l /Library/Frameworks/dwf.framework
```

## 5. What's inside the `.vip`

Peeking at the archive (`unzip -l <file>.vip`) shows the layout the installer uses and a `spec`
file. The key facts:

- Installs to `LabVIEW/vi.lib/DigilentWF/` with subfolders `common`, `FGEN`, `MSO`, `DMM`,
  `Digital`, `PS`, plus example VIs to `LabVIEW/examples/DigilentWF/` (including a **Bode Analyzer
  Example**).
- The libraries most projects reference are `common/WF-Common.lvlib`, `FGEN/WF-FGEN.lvlib`,
  and `MSO/WF-MSO.lvlib`.
- It bundles **no native library** — it relies on the system `dwf`, i.e. the framework inside
  `WaveForms.app`.
- `spec` declares `Exclusive_OS="Windows x64"` and `Exclusive_LabVIEW_Version="LabVIEW>=21.0"`,
  and lists supported hardware: Analog Discovery Studio Max, Analog Discovery Studio, Analog
  Discovery 3.

## 6. The fix — `install_digilentwf_mac.sh`

The script (in this repo) does four things, all of which require `sudo` because the targets are
owned by `root`:

1. Extracts `DigilentWF/` from the `.vip` and copies it into `…/LabVIEW <ver>/vi.lib/DigilentWF/`.
2. Copies the example VIs into `…/LabVIEW <ver>/examples/DigilentWF/`.
3. Sets ownership to `root:wheel` to match the rest of the LabVIEW install.
4. Symlinks `/Library/Frameworks/dwf.framework` → the framework inside `WaveForms.app`, so the
   native hardware calls resolve on macOS.

```bash
#!/bin/bash
# Manual macOS install of the Digilent WaveForms Toolkit for LabVIEW.
# The official .vip is Windows-only, so we hand-place the VIs that VIPM
# would normally install, plus link the WaveForms SDK framework.
# Run with: sudo bash install_digilentwf_mac.sh
set -euo pipefail

# --- Adjust these if your versions/paths differ ----------------------------
VIP="$(ls -t "$HOME"/Downloads/digilent_waveforms_vis-*.vip 2>/dev/null | head -1)"
LV="/Applications/National Instruments/LabVIEW 2026 64-bit"
WF_FW="/Applications/WaveForms.app/Contents/Frameworks/dwf.framework"
# ---------------------------------------------------------------------------
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

echo "==> Sanity checks"
[ -n "$VIP" ] && [ -f "$VIP" ] || { echo "ERROR: no digilent_waveforms_vis-*.vip in ~/Downloads"; exit 1; }
[ -d "$LV/vi.lib" ] || { echo "ERROR: LabVIEW vi.lib not found at $LV"; exit 1; }
[ -d "$WF_FW" ]     || { echo "ERROR: WaveForms framework not found at $WF_FW (install WaveForms.app)"; exit 1; }
echo "    using package: $VIP"

echo "==> Extracting DigilentWF VIs + examples from the package"
unzip -q "$VIP" "File Group 0/vi.lib/DigilentWF/*" "File Group 0/examples/DigilentWF/*" -d "$STAGE"
SRC="$STAGE/File Group 0"

echo "==> Installing libraries  -> $LV/vi.lib/DigilentWF"
rm -rf "$LV/vi.lib/DigilentWF"
cp -R "$SRC/vi.lib/DigilentWF" "$LV/vi.lib/DigilentWF"

echo "==> Installing examples   -> $LV/examples/DigilentWF"
rm -rf "$LV/examples/DigilentWF"
cp -R "$SRC/examples/DigilentWF" "$LV/examples/DigilentWF"

echo "==> Matching ownership to the rest of the LabVIEW install (root:wheel)"
chown -R root:wheel "$LV/vi.lib/DigilentWF" "$LV/examples/DigilentWF"

echo "==> Linking WaveForms SDK framework to the standard SDK location"
if [ -e /Library/Frameworks/dwf.framework ]; then
  echo "    /Library/Frameworks/dwf.framework already exists — leaving it untouched"
else
  ln -s "$WF_FW" /Library/Frameworks/dwf.framework
  echo "    linked /Library/Frameworks/dwf.framework -> $WF_FW"
fi

echo
echo "==> DONE. Verification:"
echo "    DigilentWF subfolders:"; ls "$LV/vi.lib/DigilentWF"
for lib in common/WF-Common.lvlib FGEN/WF-FGEN.lvlib MSO/WF-MSO.lvlib; do
  [ -f "$LV/vi.lib/DigilentWF/$lib" ] && echo "      OK  $lib" || echo "      MISSING $lib"
done
echo "    Framework link:"; ls -l /Library/Frameworks/dwf.framework
```

Run it:

```bash
sudo bash install_digilentwf_mac.sh
```

Then open your `.lvproj` in LabVIEW and open the main VI — the `DigilentWF` VIs should resolve and
the run arrow should be solid.

## 7. Undo / reinstall

```bash
# Remove the manual install:
sudo rm -rf "/Applications/National Instruments/LabVIEW 2026 64-bit/vi.lib/DigilentWF" \
            "/Applications/National Instruments/LabVIEW 2026 64-bit/examples/DigilentWF" \
            /Library/Frameworks/dwf.framework

# Reinstall / repair (e.g. after a LabVIEW update): just re-run the script.
sudo bash install_digilentwf_mac.sh
```

## 8. Known caveats & maintenance

- **Non-standard install.** Not managed by VIPM/NIPM. A LabVIEW update or reinstall can wipe
  `vi.lib/DigilentWF`; re-run the script to restore it.
- **The framework is a symlink** into `WaveForms.app`. If you move, rename, or uninstall WaveForms,
  the link breaks and you'll get "could not load library dwf" at run time — re-run the script (or
  repoint the symlink).
- **Keep the WaveForms Runtime (incl. Adept) installed** — it's a hard prerequisite.
- **`dwf.dll` vs `dwf.framework`.** The VIs' Call Library nodes were authored for Windows
  (`dwf.dll`). The framework symlink at the standard SDK path is what lets macOS LabVIEW load the
  native library instead. If you still hit library-load errors, double-check that link.
- **Reliable alternative:** run the project on **Windows**, where the toolkit installs normally
  through VIPM.

## License

MIT — see [LICENSE](LICENSE). Free to use, copy, and adapt.

---

*Notes contributed to help others hitting the same wall. Verified on macOS with LabVIEW 2026 and an
Analog Discovery Studio Max. Tweak the `LV` path/version in the script to match your setup.*
