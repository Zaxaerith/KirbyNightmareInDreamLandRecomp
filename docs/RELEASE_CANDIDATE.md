# Windows x64 v0.1.0-preview — local Release Candidate

Prepared on 2026-10-09. No GitHub push, remote repository, tag or remote release
was created. The native player package is under
`release-stage/KirbyNightmareInDreamLandRecomp-windows-x64-v0.1.0-preview/` and the
ZIP/`.sha256` companions sit beside it. These artifacts are excluded from Git.

The source README explains architecture, verified scope and source builds;
`recomp/player-README.md` is the player-package guide. Full file sizes/hashes
are in RELEASE_MANIFEST.md and the packaged manifest.json. Exact acceptance
results, process IDs, frame counts and pixel hashes are in RELEASE_TEST_RESULT.json.

## Acceptance

| Check | Result | Evidence/scope |
|---|---|---|
| Windows native Release build | PASS | Pinned framework/UI, GCC 16.1.0, SDL2 2.32.8; no shared-directory patches |
| Independent ZIP installation | PASS | Separate extracted installation, external CWD, PATH only Windows System32, no game.toml/developer tools |
| First-run / cached launcher | PASS | Actual hidden SDL/OpenGL renderer; dashboard, display/audio settings and controller pages captured locally |
| Input identity and cache behavior | PASS | Linked launcher model accepts valid inputs, blocks wrong/missing inputs; game entry also rejects wrong ROM/BIOS before overwriting valid caches |
| Settings persistence | PASS | Path-cache roundtrip and scale/volume persistence with unrelated settings preserved |
| Title / menu / first-stage entry | PASS | 720/1200/2800-frame snapshots identical to prior gameplay pixels |
| Native SRAM and fresh-process reading | PASS | Existing 1% / stage-2 progress, 2660-frame map then new-process 1200-frame menu, normal exits, unchanged 32 KiB SRAM hash |
| Zero-argument player Play handoff | PASS | Built-in synthetic launcher click, real windowed game, EXE-relative save, normal close; 206 presented frames |
| Stage/ZIP exclusion audit | PASS | Exact 43-file allowlist, per-file integrity, no private asset hashes or developer paths |
| Manual launcher/keyboard play | PENDING | Automated rendering/model/Play checks are not human mouse/keyboard tests |

The complete 7508-frame stage-clear replay was not repeated. Previous natural
scene transitions and progress creation remain recorded as prior-round PASS;
this RC specifically verifies the shorter regressions and retention of that
actual progress. The owner has since personally confirmed basic controller,
graphics and sound, superseding the older pending basic-audio assessment.

## Implementation and packaging decisions

- Reuse mstan recomp-ui and the generic framework launcher seam; no custom UI
  system or game-behavior patches. Normal saves are EXE-relative, while explicit
  developer CLI invocation remains available.
- Project-local framework/UI submodules use the same exact pins as the completed
  Metroid Fusion release workflow. Generator/runtime compatibility required
  genuine regeneration; the old duplicate corpus was preserved in the external pre-publication
  archive, and current full C++ remains in `generated/`.
- Game-owned strict ROM/BIOS checks cover CLI as well as the launcher. The generic
  framework's optional BIOS warn-and-try behavior and pre-gate cache writes are
  not used to weaken this cartridge's identity. No framework patch was needed.
- The executable and DLLs are stripped of debug information. All non-system
  dependencies are bundled. PE imports and a cleaned PATH were checked.
- Only README.md and manifest.json changed after successful binary/gameplay
  acceptance, to supply the dedicated player guide. Final ZIP and stage audit
  passed; every binary and launcher asset was verified byte-identical to the
  accepted installation. No gameplay replay was repeated for that document edit.
- A single player-handoff assertion initially expected verbose `rom_loaded`
  output, which the normal quiet window mode omits. The game had actually reached
  719 presented frames and closed normally. The corrected bounded check used
  the emitted cartridge coverage identity and recorded normal exit explicitly.

## Remaining limitations and publication preparation

No current technical blocker prevents using this local RC. Tested gameplay is
limited to the first stage and retained stage-2 unlock; later gameplay and
long-session save reliability remain unverified. The EXE is unsigned. Manual
launcher/keyboard interaction and extended audio fidelity remain pending.

Component licenses were checked from actual local/pinned texts, with JRickey's
MIT text obtained from its upstream. GBARecomp's PolyForm Noncommercial terms,
UI/ImGui/arm-core MIT notices, SDL zlib, GCC Runtime Library Exception, MinGW,
font terms and MPL-covered source are included separately. No knidl code was
imported and no permission to reuse it is assumed.

Before a public release: have the owner choose the license scope for original
integration files, assess compiled game/BIOS-derived distribution rights, and
arrange applicable exact-toolchain runtime source availability. These are
publication preparations, not claims that this local candidate has a blanket
MIT/GPL license. A brief owner launch/settings check on this final ZIP and a
second Windows installation are the next useful acceptance steps; broad ROM
scanning or repeated full-stage playback is not required.

## Publication follow-up

This document records the original local RC acceptance. Public-source
preparation, the owner-selected license, cleanup and binary review are recorded
in PUBLICATION.md. The original tested ZIP is retained byte-for-byte; historical
statements that no remote was created refer to the RC preparation date.
