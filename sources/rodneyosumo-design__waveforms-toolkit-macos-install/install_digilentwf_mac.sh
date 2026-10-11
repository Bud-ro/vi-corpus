#!/bin/bash
# Manual macOS install of the Digilent WaveForms Toolkit for LabVIEW.
# The official .vip is Windows-only, so we hand-place the VIs that VIPM
# would normally install, plus link the WaveForms SDK framework.
#
# Prerequisites:
#   - WaveForms.app installed (provides the native dwf library + Adept Runtime)
#   - digilent_waveforms_vis-*.vip downloaded into ~/Downloads
#       https://www.vipm.io/package/digilent_waveforms_vis/
#
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
