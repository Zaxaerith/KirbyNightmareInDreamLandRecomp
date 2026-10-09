# v0.1.0-preview — Windows x64 Experimental Preview

Publication draft: attach only the approved ZIP after the binary review gate
in PUBLICATION.md is resolved. This draft does not create a Tag or Release.

## Overview

A native Windows integration of Kirby: Nightmare in Dream Land (USA Rev 0),
built with pinned GBARecomp and recomp-ui. Cartridge ARM/Thumb code is compiled
ahead of time into x64 code; an ARMv4T interpreter handles uncovered paths.
GBA hardware behavior is supplied by the runtime. **This is not FULLY_STATIC
and full-game compatibility is not claimed.**

## Installation

1. Download and extract the Windows x64 ZIP into a writable folder.
2. Keep the EXE, four DLLs, assets and licenses together; run
   `KirbyNightmareInDreamLandRecomp.exe`.
3. Select your own legally obtained ROM and retail GBA BIOS. Strict identity
   checks block unsupported or missing files. Valid paths are remembered.
4. Configure controls, display and volume, then press Play.

Players do not need a compiler, CMake, Ninja, Python or a development checkout.
Use Windows 10/11 x64 with a suitable desktop graphics driver. The EXE is
unsigned. ROM and BIOS files are **not included** in the download.

| Input | Identity | Bytes | SHA-1 |
| --- | --- | ---: | --- |
| ROM | Kirby: Nightmare in Dream Land, USA Rev 0, A7KE | 8,388,608 | `37a476567d133c146fee6b5e2eb0b07a215da6b0` |
| BIOS | Retail GBA BIOS | 16,384 | `300c20df6731a33952ded8c436f7f186d25d3492` |

## Verified scope

- BIOS boot, title and original menus.
- Vegetable Valley stage 1-1 basic operations, three natural door transitions
  and completion through the original Goal Game.
- Real native SRAM progress: File 1 at 1%, stage 2 unlocked, retained after a
  normal exit and a fresh process. Save States were not used.
- Owner-confirmed controller operation, basic graphics and sound.
- Independent extracted RC startup without developer tools, strict valid/wrong
  input handling, cached paths/settings and short title/stage/save regressions.

## Controls and storage

Default keyboard: arrows for movement, X for GBA A, Z for B, Enter for Start,
Right Shift for Select, C/V for L/R. Compatible SDL2 controllers are supported;
launcher mappings are editable. The launcher also exposes display and audio
settings. Native saves use `saves/kirby_nightmare_usa.sav` beside the EXE.
Close normally after the game's save sequence and back up SRAM before updates.
Private cached paths/settings stay beside the EXE and are not package content.

## Known limitations

Later stages, bosses, multiplayer and full completion are unverified.
Long-session save reliability, extended audio fidelity and manual
keyboard/launcher interaction remain outside automated acceptance.
Interpreter fallback remains; no compiler is required at runtime.
No widescreen, advanced graphics patch, updater or signing is promised.

## Source, credits and component terms

Source and Windows regeneration/build instructions:
https://github.com/Zaxaerith/KirbyNightmareInDreamLandRecomp

Original integration files are PolyForm Noncommercial 1.0.0, Copyright 2026
Zaxaerith; third-party components retain their exact licenses and notices.
Thanks to Matthew Stanley/GBARecomp/recomp-ui, SDL, Dear ImGui, GCC/MinGW,
toml++ and font contributors. overjt/knidl is credited for separate research;
none of its implementation or bulk symbol data is included.

This unofficial project is unaffiliated with Nintendo or HAL Laboratory.
Their game, BIOS and trademarks remain their property. The integration license
grants no game-content rights. Consult the approved distribution review and
bundled component notices; a checksum or input-file exclusion is not a rights
grant. The approved asset checksum must be supplied alongside the ZIP.

## Prepared asset (pending distribution review)

`KirbyNightmareInDreamLandRecomp-windows-x64-v0.1.0-preview.zip` - 8181899 bytes.
SHA-256: `fc699c2c99581c03b51fefb7b7b654b225f7d7d80f0a54a1d3d1271db13d35b4`.

License/player documents are updated; game binaries are byte-identical to the
accepted RC. The asset remains local and has not been uploaded. Preserve the
historical RC checksum separately from this prepared asset checksum.
