# vi-corpus

A large collection of `.vi`, `.ctl`, `.lvlib`, `.lvclass`, `.lvproj` and the
other files the LabVIEW™ software saves, vendored from public repositories
together with their licenses and the assets they refer to.

Each upstream repository lives under `sources/<owner>__<repo>/` with its own
tree layout preserved, so relative links between VIs, controls, libraries,
classes and projects resolve as they did upstream.

This repo provides a few additional convenience files:
- `manifest.json` provides metadata for the original sources, including:
  - Repository URL
  - Commit hash
  - SPDX identifier for the license
  - Fetch date
  - The list of files (path, size, sha256, and whether it was kept for its extension,
    as a reference from another kept file, or as part of the tree)
  - Files left out for size, and references that point outside the repository
    (`<vilib>` paths and absolute paths)
- `vi-package-manifest.json` allows for functional reproducibility of the VI Package Manager
  related files in the repo. This includes packages (`.vip`) and configurations (`.vipc`).
  For each one it records the raw-download URL at the vendored commit, size and sha256,
  every zip member with its size, CRC-32 and sha256, and the text of the `spec` and
  `config.xml` members. The packages are zip files of LabVIEW files that are already in the
  repo: across every package recorded, 95.7% of the LabVIEW files inside have a same-named
  file in the tree, and the remainder are third-party dependency packages shipped alongside
  the source. NOTE: a `.vi` re-saved into a package keeps its saving version but differs
  from the tree's copy by a few hundred bytes.
- `sources.json` lists every vendored source
- `candidates.json` lists public repos that could not be vendored due to missing licenses,
  unsuitable licenses, potential NI product content, etc.
- `corpus.json` names the file extensions the corpus collects.

This repo does NOT include installers, archives, VI Package Manager packages, FPGA bitfiles,
build and IDE caches, office documents, video, 3D models and unreferenced files over 1 MB.

## Legal

Files are redistributed under their upstream licenses only. See `manifest.json`
for the original licenses.

The original files in this repo are licensed under the MIT license.

LabVIEW™ is a trademark of National Instruments. This collection is not
affiliated with, endorsed by, or sponsored by National Instruments; the name is
used only to identify the file formats the files are saved in. See NI's
[trademark and logo guidelines](https://www.ni.com/en/about-ni/legal/trademarks-and-logo-guidelines.html).

## Checking out a Few Sources

This repo is about 3 GB in the Git pack. Additionally the working tree is over 8 GB.
To save yourself on bandwidth and disk size, you can use the sparse checkout feature:

```
git clone --filter=blob:none --sparse https://github.com/Bud-ro/vi-corpus
cd vi-corpus
git sparse-checkout set sources/picotech__picosdk-ni-labview-examples
```
