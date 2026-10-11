# Packagoing PPLs (Multi-Platform)

Problem Statement:

> I'm building a toolkit that has 32-bit and 64-bit versions of a few ppls. I want one single VIP that can target either/both LabVIEW bitnesses but I don't think VIP Builder supports this? (VIPM 2020). Do I need two VIP packages - one for 32-bit one for 64-bit?
> Found this forum post suggesting it's possible with the aid of some unreleased tools from Jim: https://forums.vipm.io/topic/4235-how-to-build-vi-packages-which-supports-multiple-target-platforms/ Haven't looked at those tools yet - wanted to check in first - is this supported yet?

Proposed Solution:

- rename each platform-specific PPL something like: `my_library.lvlibp.linux_x86`, `my_library.lvlibp.windows_x86`, `my_library.lvlibp.windows_x64`
- keep all of these next to the PPL for your platform. e.g. if you're working in 64-bit LabVIEW on Windows, then your active PPL named `my_library.lvlibp` will be identical to `my_library.lvlibp.windows_x64`
- if you want, you can keep all these platform-specific PPLs in a subfolder, but they should all be installed and in a location you can easily find, post-install
- create a post install custom action that finds PPLs in the installed files and for each PPL it finds, checks if there is a platform-specific PPL and copies it over the active PPL. e.g. if I were installing the package on linux it would delete then copy `my_library.lvlibp.linux_x86` as `my_library.lvlibp` (replacing the existing `my_library.lvlibp`).
- optionally, this post-install script could delete all files matching `my_library.lvlibp.*_*` since they are no longer needed. However, they can probably just be left there since they aren't hurting anything (as they do not have valid LabVIEW file type extensions)
