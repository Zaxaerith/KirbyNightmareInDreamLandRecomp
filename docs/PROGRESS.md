# Verified progress — stable v0.1.0-preview

This public summary preserves the stable RC evidence without internal machine
paths, raw logs, screenshots or private input files. Original detailed history
and the knidl study remain in a private archive and local research branch.

## Native integration

- Windows x64 Release build using GCC 16.1.0, CMake 4.4.4, Ninja 1.13.2 and
  SDL2 2.32.8; pinned dependencies in FRAMEWORK_PIN.json.
- 5,470 cartridge AOT functions in 16 shards, plus locally recompiled retail
  BIOS. ARMv4T interpreter fallback remains; NOT_STATIC is expected.
- Strict USA Rev 0 A7KE ROM and retail BIOS identity gates for launcher and CLI.
- Existing recomp-ui supplies cached private paths and player settings;
  compiler/self-heal generation is not required during normal player launches.

## Gameplay evidence

| Check | Result | Scope |
| --- | --- | --- |
| BIOS boot, title and file/game menus | PASS | Original flow and framebuffer |
| First-stage movement, jump, flight, inhale/spit | PASS | Vegetable Valley stage 1-1 |
| Natural region transitions | PASS | Three original star-door transitions |
| First-stage completion | PASS | Original Goal Game; 7,508-frame deterministic input path |
| Native progress creation | PASS | File 1 at 1%, stage 2 unlocked |
| Native progress cold reading | PASS | New process, normal exits, real 32 KiB SRAM; no Save State |
| Owner controller, basic graphics and sound | PASS | Personally confirmed by project owner |
| Manual keyboard/launcher interaction | PENDING | Automated scripts do not certify human operation |
| Later stages, bosses and complete game | UNTESTED | No full-game claim |
| Extended audio fidelity and long-session saves | PENDING | Outside current acceptance |

The verified SRAM contains 32,768 bytes, SHA-256
`887b18cd75b8b05e905f7f74a2f5bc01ddc5386eede466ae5c5e7014ab8d6312`.
This hash identifies private evidence, not a distributed save file.

## Independent RC acceptance

The final installation contains 43 allowlisted files and no ROM/BIOS files,
private SRAM, caches, generated C++, developer paths or build tools. Tested
from an extracted installation and unrelated working directory, with only
Windows System32 on PATH:

- Hidden first/cached launcher renderer and strict input/settings model PASS.
- Wrong ROM/BIOS processes reject inputs without replacing valid cached paths.
- Title at 720 frames and first-stage entry at 2,800 frames are pixel-identical
  to earlier accepted evidence.
- Existing progress map at 2,660 frames and a fresh-process file menu at 1,200
  frames are pixel-identical to earlier saved-progress evidence. SRAM hash is
  unchanged after both normal exits.
- Synthetic launcher Play handoff reaches real windowed gameplay and closes
  normally; manual operation remains a separate check.

RELEASE_TEST_RESULT.json records process IDs, frames and pixel hashes;
RELEASE_MANIFEST.md records the final file inventory and hashes. These are
historical RC acceptance records, not new publication-time gameplay tests.
The complete stage-clear replay was not repeated for publication preparation.

## Public-source preparation

Stable runtime/host/game code is based on private RC commit `f8b725a`.
Public main is a sanitized source snapshot with a separate root, preserving
original local history without uploading old developer-machine paths or the
`feature/knidl-symbols` branch. No experiment implementation, bulk symbols or
knidl source is included. Generated C++ remains complete and ignored locally.
The owner selected PolyForm Noncommercial 1.0.0 for original integration files;
third-party grants remain unchanged. See PUBLICATION.md for source checks,
archive integrity and the separate binary-distribution conditions.
