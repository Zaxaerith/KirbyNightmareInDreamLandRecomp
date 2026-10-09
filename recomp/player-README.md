# KirbyNightmareInDreamLandRecomp — v0.1.0-preview

**Experimental Preview / local Release Candidate for Windows 10/11 x64.**
An unofficial native recompilation integration for Kirby: Nightmare in Dream
Land, USA A7KE revision 0. Not affiliated with Nintendo or HAL Laboratory.
Supply your own legally obtained ROM and original retail Game Boy Advance BIOS.

## Install and start

1. Extract the complete ZIP into a writable folder. Keep the EXE, all four DLLs,
   assets/ and license files together. Do not run inside the ZIP.
2. Run KirbyNightmareInDreamLandRecomp.exe. No compiler, CMake, Ninja, Python or
   developer installation is required. A desktop graphics driver with OpenGL
   support is needed for the launcher. This candidate is unsigned.
3. Browse for your own ROM and BIOS. Incorrect or missing inputs block Play.
4. Configure your controller/keyboard, display and volume, then select Play.
   Valid paths and settings are remembered. If a file moves, select it again.

To reopen a skipped launcher, run the EXE with `--launcher`.

## Supported inputs

| File | Required identity | Bytes | SHA-1 |
|---|---|---:|---|
| Game ROM | USA A7KE revision 0; header AGB KIRBY DX | 8,388,608 | 37a476567d133c146fee6b5e2eb0b07a215da6b0 |
| BIOS | Original retail GBA BIOS | 16,384 | 300c20df6731a33952ded8c436f7f186d25d3492 |

Other regions, revisions, patched ROMs and substitute BIOS images are unsupported.
No ROM/BIOS files or download links are provided.

## Controls and settings

| GBA input | Default keyboard | Typical gamepad |
|---|---|---|
| D-pad | Arrow keys | D-pad / left stick |
| A (jump) | X | Bottom face button |
| B (inhale/spit) | Z | Right face button |
| Start | Enter | Start |
| Select | Right Shift | Back/Select |
| L / R | C / V | Left / right shoulder |

Use the launcher's editable mapping for your controller. Display settings include
window scale, fullscreen and presentation/filter choices; audio provides volume.
Rendering retains the game's native 240 × 160 view. No widescreen patch is enabled.

## Saves and personal configuration

Native cartridge progress is stored in `saves/kirby_nightmare_usa.sav` next to
the EXE: original 32 KiB SRAM, not a save state. Let the game finish its saving
sequence and close normally. Forced termination can lose progress. Back up this
file before updating, and preserve it when extracting a newer build.

`rom.cfg`, `bios.cfg`, `config.ini` and `keybinds.ini` next to the EXE remember
your file paths and settings. Preserve them for updates; do not publish them.
The pristine package contains no personal paths, settings or saves.

## Verified scope and limitations

BIOS boot, title/file/game menus, first-stage controls, three natural star doors
and full stage 1-1 clear were previously verified. Original progress reached 1%
and unlocked stage 2, surviving normal exit and a new process. The RC's short
checks confirm title, first-stage entry and cold-loaded native progress; they
do not repeat the complete stage-clear replay.

The owner personally confirmed basic controller play, graphics and sound before
launcher integration. Automated launcher checks are not manual keyboard/UI play.
Later stages, bosses, multiplayer, long-session save safety and complete audio
fidelity remain unverified. Keep a backup of SRAM and the original game.

Execution uses native ahead-of-time code plus ARMv4T interpreter fallback. This
is not FULLY_STATIC. Runtime compilation is disabled by default; performance
and uncovered paths may vary. No advanced patches, updater or signing is promised.

## Package integrity and source information

The ZIP's external `.sha256` file identifies the archive. `manifest.json` lists
each bundled file's size and SHA-256, excluding itself. Package contents are an
EXE, four DLLs, eleven generic launcher assets, documentation and component
licenses/source notices. ROM, BIOS, generated game/BIOS C++, saves and private
test logs/screenshots are excluded.

Source-building instructions and technical evidence are in the source checkout's
README.md and docs/. They are not included in this player package. This candidate
has only been prepared locally; no remote release or repository was created.

## Credits, licenses and legal notice

Thanks to Matthew Stanley (GBARecomp, arm-recomp-core, recomp-ui), SDL, Dear
ImGui, GCC/MinGW and the font projects. Local Metroid Fusion and Golden Sun
integrations provided workflow/documentation examples.

Licenses apply per component. GBARecomp is PolyForm Noncommercial 1.0.0; UI and
several supporting libraries are MIT, SDL2 is zlib, mGBA-derived BIOS HLE files
are MPL-2.0, and fonts/runtime DLLs retain separate terms. Full texts and exact
MPL-covered source are in licenses/. Read THIRD_PARTY_NOTICES.md and LICENSE.md.
No blanket MIT/GPL project license is asserted. Original integration licensing
is unassigned pending the owner's choice before publication. No overjt/knidl
code was imported and no reuse permission is presumed.

The game, BIOS and trademarks belong to their respective owners. This project
grants no rights to them and claims no affiliation or endorsement. Intended use
is local noncommercial personal research/testing under the dependencies' terms.
Assess compiled-game distribution rights separately before publishing this RC.
