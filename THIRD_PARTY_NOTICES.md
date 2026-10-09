# Third-party notices — v0.1.0-preview

Full texts accompany the player package in licenses/. Source pins are recorded in docs/FRAMEWORK_PIN.json.

| Component | Actual source/version | Terms |
|---|---|---|
| GBARecomp | mstan/gbarecomp e3c834d399b66f5a823c2f0f9d878b62dc05d25a | PolyForm Noncommercial 1.0.0, Copyright 2026 Matthew Stanley, with file exceptions below |
| recomp-ui | mstan/recomp-ui 6374aae201b930c97425718249f5d39b2275ca13 | MIT, Copyright 2026 Matthew Stanley |
| arm-recomp-core | c626f4e53fcdca0c72d2a7d34d41663d87c7e175 | MIT, Copyright 2026 Matthew Stanley |
| recomp-net / rbengine | Framework-pinned nested dependencies | MIT, respective contributor notices retained; not a multiplayer verification claim |
| Dear ImGui | UI-vendored source | MIT, upstream copyright retained |
| SDL2 | 2.32.8 | zlib |
| toml++ | 30172438cee64926dc41fdd9c11fb3ba5b2ba9de | MIT; generator dependency, not required by players |
| GCC/MinGW runtime | GCC 16.1.0 local x64 toolchain | GPLv3 with GCC Runtime Library Exception; separate MinGW runtime terms |
| Lato / Noto Sans Symbols 2 | UI-bundled fonts | SIL Open Font License 1.1 |
| OpenMoji black font | UI-bundled font | CC BY-SA 4.0, OpenMoji Project |
| flags.png | UI rendering from Noto Color Emoji | SIL OFL 1.1, Noto Project Authors |

GBARecomp's THIRD_PARTY_ATTRIBUTION.md is retained. JRickey/gba-recomp-derived MP2K detection/offsets, color simulation, RTC and audio shadow portions retain MIT OR Apache-2.0 terms. The MIT option and Copyright 2026 JRickey are retained in JRickey-MIT.txt, fetched from https://github.com/JRickey/gba-recomp/blob/main/LICENSE-MIT.

Framework src/runtime/bios_hle.cpp and bios_hle.h derive from mGBA by Jeffrey Pfau and contributors and are MPL-2.0 rather than PolyForm. Their exact unmodified pinned source is included in licenses/mpl-source/ with the MPL text. Retail BIOS LLE remains default. libmgba is not linked into this release. Remaining generic source is available at https://github.com/mstan/gbarecomp/tree/e3c834d399b66f5a823c2f0f9d878b62dc05d25a.

GCC GPL/LGPL, Runtime Library Exception and MinGW notices accompany the four runtime DLLs. Before public binary publication, arrange applicable corresponding source availability for the exact runtime toolchain; no commercial license is implied.

Generic integration/release patterns were adapted from the local Metroid Fusion integration; its MIT notice is retained in Reference-Integration.txt. No Metroid game code, symbols or assets were imported. Golden Sun was a documentation reference. overjt/knidl has no granted code reuse permission; none of its code is copied, linked or vendored.

Original Kirby integration files owned by Zaxaerith use PolyForm Noncommercial
1.0.0 as scoped in LICENSE.md; full terms are in LICENSE. No third-party material
is relicensed by that grant. HAL Laboratory/Nintendo own original game content and marks. ROM, BIOS, generated cartridge/BIOS C++, personal saves and internal test evidence are excluded. No affiliation or endorsement is claimed.

## Public binary review

The public source preserves exact dependency URLs/pins and required notices.
The original RC ZIP predates the owner-selected integration license and still
contains historical candidate documentation. Its unchanged hash is an acceptance
record, not proof that distribution conditions have been resolved. Before a
binary release, record the ROM/BIOS-derived executable rights assessment and
applicable corresponding-source arrangements for the exact runtime DLLs.
See docs/PUBLICATION.md.
