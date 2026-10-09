# KirbyNightmareInDreamLandRecomp

A Windows x64 native recompilation integration for **Kirby: Nightmare in Dream Land (USA, A7KE, revision 0)**, using [GBARecomp](https://github.com/mstan/gbarecomp) and [recomp-ui](https://github.com/mstan/recomp-ui).

**v0.1.0-preview — Experimental Preview.** This unofficial project is not affiliated with HAL Laboratory or Nintendo. Supply your own legally obtained ROM and GBA BIOS. Full-game compatibility is not claimed. Public integration source is provided here; the accepted binary candidate remains subject to the distribution review described in [docs/PUBLICATION.md](docs/PUBLICATION.md).

Kirby: Nightmare in Dream Land is the Game Boy Advance remake of Kirby's Adventure. This integration preserves the original game's rules, stages and native SRAM while running translated ARM/Thumb routines on Windows. It aims to make the verified early game playable without requiring players to install development tools.

## Verified playable scope

- Retail BIOS boot, title, file/game menus and Vegetable Valley stage 1-1.
- Walking, jumping, flight, inhale/spit, three natural star-door transitions and stage 1-1 completion through the original Goal Game.
- Original cartridge SRAM progress: File 1 at 1%, stage 2 unlocked, both retained in a new Windows process after normal exit. No save states established these results.
- The owner personally played and confirmed basic controller input, graphics and sound. Manual keyboard play and extended audio fidelity remain unverified.

See [docs/PROGRESS.md](docs/PROGRESS.md) for evidence and [docs/RELEASE_TEST_RESULT.json](docs/RELEASE_TEST_RESULT.json) for the RC checks. Later stages, bosses, multiplayer and full completion are outside the verified scope. This RC uses short regressions and does not repeat the 7,508-frame stage-clear replay.

## Technical implementation

The generator translates discovered cartridge ARM/Thumb code and the real BIOS into C++, which is compiled into a native x64 executable. GBARecomp supplies the guest bus, PPU, APU, timers, DMA, interrupts and cartridge save device. SDL2 supplies host video, sound and input.

Execution combines ahead-of-time code with ARMv4T interpreter fallback for uncovered paths. This preview is **not FULLY_STATIC**. Runtime self-heal compilation is disabled by default: players need no compiler. It retains native 240 × 160 rendering and original game flow, without widescreen patches or guest-state shortcuts.

The framework/UI are pinned project submodules matching the local Metroid Fusion release workflow. [docs/FRAMEWORK_PIN.json](docs/FRAMEWORK_PIN.json) records the revisions and generator's toml++ dependency. Generic licensed integration patterns were reused; no Metroid-specific behavior, symbols or assets were imported.

## Installation and first launch

Check the repository's [Releases page](https://github.com/Zaxaerith/KirbyNightmareInDreamLandRecomp/releases) for available Windows downloads. A locally tested RC is not automatically a published download; if no asset is available, follow the source-build steps below. ROM and BIOS are never provided as download assets.

1. Extract `KirbyNightmareInDreamLandRecomp-windows-x64-v0.1.0-preview.zip` into a writable folder. Keep the EXE, four DLLs, `assets/` and licenses together.
2. Run `KirbyNightmareInDreamLandRecomp.exe`. Players do not need CMake, Ninja, GCC, Python or a developer checkout.
3. Select your supported ROM and retail GBA BIOS in the launcher. Both are strictly verified against the hashes below. Missing/wrong inputs block Play.
4. Review controller/keyboard, display and audio settings, then select Play. Valid paths and settings are remembered.

Use Windows 10/11 x64 with a desktop graphics driver. Do not run inside the ZIP or install into a read-only folder. The EXE is unsigned. If a remembered file moves, select its new location. To reopen a skipped launcher, run `KirbyNightmareInDreamLandRecomp.exe --launcher`. No Nintendo box art is bundled.

## Required private files

| Input | Supported identity | Bytes | SHA-1 |
|---|---|---:|---|
| ROM | USA A7KE revision 0; header `AGB KIRBY DX` | 8,388,608 | `37a476567d133c146fee6b5e2eb0b07a215da6b0` |
| BIOS | Original retail Game Boy Advance BIOS | 16,384 | `300c20df6731a33952ded8c436f7f186d25d3492` |

Other regions, revisions, modified ROMs and HLE BIOS replacements are unsupported. Renaming a file does not make it valid. See [baserom.md](baserom.md). This project provides no ROM/BIOS download links.

## Controls, display and audio

The launcher provides keyboard/gamepad mapping, window scale/fullscreen, display presentation/filter options and volume. Review your controller mapping before playing; a compatible SDL2 gamepad is recommended.

| GBA input | Default keyboard | Typical gamepad |
|---|---|---|
| D-pad | Arrow keys | D-pad / left stick |
| A (jump) | X | Bottom face button |
| B (inhale/spit) | Z | Right face button |
| Start | Enter | Start |
| Select | Right Shift | Back/Select |
| L / R | C / V | Left / right shoulder |

Controller conventions vary; editable launcher mapping is authoritative. Keyboard input is implemented and replay-tested, but manual keyboard play is not independently certified. The launcher requires a normal desktop OpenGL-capable graphics driver; some headless/remote sessions may not render it.

## Native saves and settings

Normal player launches save to **`saves/kirby_nightmare_usa.sav` beside the EXE**. This is the original 32 KiB cartridge SRAM, not a machine state. Allow the game's progress-saving sequence to finish and close normally; forced termination may lose changes. Back up SRAM before replacing builds. Creating an SRAM file alone is not proof of progress: the verified results are the game's 1% indicator and unlocked stage 2 after cold boot.

`rom.cfg`, `bios.cfg`, `config.ini` and `keybinds.ini` beside the EXE are player configuration. They may contain personal paths. Preserve them when updating, but do not publish them. The pristine ZIP contains no configuration or saves. Double-click/`--launcher` launches use the EXE directory; explicit developer CLI arguments retain normal working-directory behavior.

## Build from source on Windows

Use native PowerShell, Git, CMake 3.20+, Ninja, MinGW-w64 x64 GCC and SDL2's **MinGW development** package. MSVC import libraries are not a substitute for SDL2's MinGW libraries. The RC uses GCC 16.1.0, CMake 4.4.4, Ninja 1.13.2 and SDL2 2.32.8. Python 3 is needed only for package auditing/tests. This workflow uses neither WSL nor Docker.

Install the toolchain and extract SDL2 development files yourself; the scripts do not install system software. Put `git`, `cmake`, `ninja`, and the MinGW `bin` directory on PATH. `-Toolchain` names the MinGW root containing `bin/gcc.exe` and `bin/g++.exe`; `-SdlRoot` names SDL2's `x86_64-w64-mingw32` directory containing `include/SDL2`, `lib/libSDL2.dll.a` and `bin/SDL2.dll`.

```powershell
git clone https://github.com/Zaxaerith/KirbyNightmareInDreamLandRecomp.git
Set-Location KirbyNightmareInDreamLandRecomp
git submodule update --init --recursive
./tools/setup-deps.ps1
# Put cmake, ninja, git and MinGW bin on PATH.
./tools/build-host.ps1 -GeneratorOnly -Toolchain C:/path/to/mingw64 -SdlRoot C:/path/to/SDL2/x86_64-w64-mingw32
./tools/regen.ps1 -Rom C:/private/kirby.gba -Bios C:/private/gba_bios.bin
./tools/build-host.ps1 -Jobs 4 -Toolchain C:/path/to/mingw64 -SdlRoot C:/path/to/SDL2/x86_64-w64-mingw32
./build/host/KirbyNightmareInDreamLandRecomp.exe
```

Generator-only configuration works before cartridge output exists. Generation writes `generated/cart/` and `generated/bios/`; the script also stages a generic BIOS support header when the selected framework provides one. Complete generated C++ remains local and ignored by Git. `game.toml` is developer configuration, not a required player asset. Use explicit private paths rather than existing local convenience defaults. Framework and toml++ are project-local; SDL/compiler locations are configurable.

The repository contains no generated cartridge or BIOS C++; regeneration with your own verified files is required. `setup-deps.ps1` fetches the exact toml++ commit in `docs/FRAMEWORK_PIN.json` and checks dependency identities. Recursive submodule initialization also fetches the framework's Android SDL submodule; that checkout is not used for this Windows build. Windows SDL2 development files remain a separate prerequisite. A different GCC version or dependency pin has not been certified by the RC acceptance.

The accepted complete native build is documented in [docs/RELEASE_CANDIDATE.md](docs/RELEASE_CANDIDATE.md). Publication checks distinguish clean source/dependency setup from full cold regeneration and compilation; see [docs/PUBLICATION.md](docs/PUBLICATION.md). Do not infer a full cold build from a successful clone alone.

### Source layout

| Path | Purpose |
|---|---|
| `src/` | Project-owned host entry, launcher adaptation and strict input validation |
| `CMakeLists.txt`, `tools/` | Windows generator, regeneration, build and package workflow |
| `game.toml`, `baserom.md` | Supported ROM identity and generation configuration |
| `gbarecomp/`, `recomp-ui/` | Exact licensed submodule dependencies |
| `docs/` | Dependency pins, concise validation and release inventory |
| `generated/`, `build/`, `logs/` | Ignored local translations, binaries and evidence |

Short developer smoke:

```powershell
./tools/run-smoke.ps1 -Frames 720 -Name title -Rom C:/private/kirby.gba -Bios C:/private/gba_bios.bin
./tools/run-smoke.ps1 -Frames 2800 -Replay ./tools/first-actions.csv -Name entry -Rom C:/private/kirby.gba -Bios C:/private/gba_bios.bin
```

Smoke saves/logs/screenshots stay under ignored `logs/`. Use fresh names for fresh saves. `tools/first-stage-clear.csv` preserves the complete acceptance path for targeted investigations, not routine rebuilds.

## Make and verify a local package

```powershell
./tools/make-release.ps1 -SkipBuild -Toolchain C:/path/to/mingw64 -SdlRoot C:/path/to/SDL2/x86_64-w64-mingw32 -Python python
python ./tools/test-release.py ./release-stage/KirbyNightmareInDreamLandRecomp-windows-x64-v0.1.0-preview.zip --rom C:/private/kirby.gba --bios C:/private/gba_bios.bin --save C:/private/verified-progress.sav
```

Packaging verifies dependency pins and Release configuration, stages an explicit allowlist, strips debug information, writes a per-file SHA-256 manifest, audits stage/ZIP and writes a ZIP `.sha256` companion. It refuses to overwrite existing output. The manifest excludes itself to avoid a circular hash.

Tests extract a separate installation, remove developer tools from PATH and use disposable SRAM copies. Hidden launcher rendering/model checks are distinguished from manual UI operation. No private input is added to the ZIP.

## Credits and licenses

Thanks to Matthew Stanley for GBARecomp, arm-recomp-core and recomp-ui; SDL, Dear ImGui, toml++, GCC/MinGW and the font projects; and the local Metroid Fusion/Golden Sun integrations for build and documentation examples.

Licenses apply per component, without a blanket MIT/GPL project claim. GBARecomp is PolyForm Noncommercial 1.0.0; recomp-ui, arm-recomp-core and Dear ImGui are MIT; SDL2 is zlib. mGBA-derived BIOS HLE files are MPL-2.0 and their exact source is bundled under `licenses/mpl-source/`. JRickey-derived framework portions retain MIT attribution. Fonts and GCC/MinGW runtime terms are included separately. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSE.md](LICENSE.md).

Original integration code, scripts and documentation are licensed by Zaxaerith under **PolyForm Noncommercial 1.0.0**, as scoped in [LICENSE.md](LICENSE.md), with the full text in [LICENSE](LICENSE). Third-party code retains its own grants and notices. Thanks also to overjt/knidl for separate decompilation research; this stable distribution includes none of its implementation or bulk symbol data, and assumes no reuse permission.

The original game/BIOS and trademarks belong to their owners. This unofficial project grants no game-content rights. Intended use is local noncommercial research/personal testing under applicable dependency terms. Any distribution of a compiled game-derived executable needs separate rights assessment; a private-file exclusion audit does not resolve it.

## Experimental Preview limitations

- Verified game scope ends at stage 1-1 and the unlocked stage 2 gate.
- Interpreter fallback is expected; performance and uncovered paths may vary.
- Later stages, long-session save reliability and complete audio fidelity are untested.
- Manual launcher operation/manual keyboard play are not claims of automated RC checks. The owner's controller/audio confirmation predates launcher integration.
- No multiplayer, widescreen, advanced patches, signing or updater is promised.
- Source publication and binary distribution have separate acceptance conditions; see [docs/PUBLICATION.md](docs/PUBLICATION.md).

Back up SRAM and retain the original game for comparison. Report version and reproducible steps without sharing private game files or personal configuration.
