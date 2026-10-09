# Public-source preparation and binary release gate

## Stable source and preserved history

Public main starts from the stable RC source snapshot at private commit
`f8b725ab5140eb01aaeb379a2dc5157dbd64eeeb`. The original commit contained four
machine-specific path references; main therefore has a sanitized independent
root. The original master and `feature/knidl-symbols` at
`736abdfab7268ac47eab4d97ad237df40ae35041` remain local and archived. Neither is
pushed. There is no merge of the symbol experiment and no force push.

Host C++, game configuration and the CMake runtime setup remain the stable RC
versions. Publication changes concern documentation, original-code licensing,
ignore rules and explicit portable SDK/input paths. Generated cartridge/BIOS
C++, private assets/saves, binaries, cached settings, raw evidence, upstream
knidl material and bulk names are absent from the public source and history.

The owner selected PolyForm Noncommercial 1.0.0, Copyright 2026 Zaxaerith,
for original integration code/scripts/documentation on 2026-10-09. Third-party
notices and licenses remain separate. LICENSE contains the full original-code
terms; LICENSE.md explains their scope.

## Historical archive and cleanup

Before cleanup: 678,075,415 bytes, 3,384 files, 1,121 directories (including
project dependency and Git directories). A complete project archive was created
outside the checkout, including `.git`, both original branches and all private
research/test data:

`KirbyNightmareInDreamLandRecomp_prepub_20261009.7z`

Archive size: 205,986,460 bytes. 7-Zip full integrity test PASS.
SHA-256: `55cb9974ebd61584cbd2e74ebb3dc7a035c7c3f9827dd920cef305d1b25d7b2b`.

A path-validated, 98-item cleanup plan removed old baseline/experimental build
copies, individual compiler caches, three superseded stages, three extracted
acceptance installations, one intermediate ZIP and temporary logs/screenshots.
No whole build/generated/research root was recursively removed. Six scratch
SRAM copies were moved out with hash checks before deleting their test folders.
Root/regular-test saves and original ROM/BIOS remain unchanged. Complete current
`generated/`, the accepted host/generator EXEs, final staged package, original
ZIP/hash and manifest remain available locally; 92 original files were
hash-verified after cleanup.

knidl materials and reports were moved outside the project and remain private.
The archive, detailed inventory, cleanup plan and relocated-save records are
not repository content. They contain private inputs and must never be uploaded
as release assets. After-cleanup totals and final check status are recorded in
PUBLICATION_CHECKS.json when the checks finish.

## Clean source build verification

Exact framework and UI commits were confirmed available through their upstream
GitHub commit endpoints. An independent source clone, recursive submodule initialization, pinned
dependency setup and a 45-step native Release generator build all passed. The
initial full-history toml++ download failed with a TLS disconnect; the corrected
script successfully fetched only the pinned commit with a bounded request.
Complete ROM/BIOS regeneration and game compilation were not repeated. Required external software: native Git/PowerShell, CMake,
Ninja, MinGW-w64 and SDL2 MinGW development files; Python for package audits.
No system software installation or other-game project changes are performed.

The complete original RC native build and player acceptance already passed.
Publication checks do not repeat the full 7,508-frame gameplay replay. They do
not claim a full cold build unless all regeneration and game compilation steps
were actually executed; see PUBLICATION_CHECKS.json for the exact scope.

## Binary gate — pending evidence

The owner indicates that rights/source-provision evidence exists; its details
have not yet been supplied or verified. No Tag or public binary Release should
be created until the following are documented:

1. The rights/assessment basis for distribution of the executable's translated
   game and retail BIOS code. Omitting the original input files does not, by
   itself, settle rights in their derived compiled code.
2. The applicable corresponding-source/provision conditions for exact bundled
   GCC/MinGW runtime DLLs. Installed GCC reports the MinGW-Builds project,
   GCC 16.1.0, x86_64 win32 SEH UCRT, revision 0; obtain the matching upstream
   source/build provenance rather than assuming any GCC source tarball matches.
3. Alignment of player-package documentation with the owner's newly selected
   license. The original RC ZIP predates that decision. If documents are updated,
   preserve the original ZIP and record a new checksum; do not rebuild unchanged
   gameplay binaries or repeat full-stage acceptance just for documentation.

The [GCC runtime exception](https://gcc.gnu.org/onlinedocs/libstdc++/manual/license.html)
permits eligible independent compiled combinations under their own terms; it
is not a blanket permission to ignore the separate runtime-library obligations.
The pinned PolyForm framework grant concerns the framework, not Nintendo/HAL
or retail BIOS rights. MPL-covered BIOS HLE source is already in the accepted
package, with its own terms. No knidl implementation is part of this release.

The unchanged accepted ZIP is 8,179,728 bytes, SHA-256
`8fc8b8c7f1c1e70dec6489f2ee24a4e3fadc238b19f6d3c071ba5c262af234f2`.
It passes its 43-file allowlist/manifest audit. This audit establishes integrity
and input-file exclusion, not authorization to distribute compiled derivatives.

RELEASE_NOTES.md prepares English preview notes. After the gate is resolved,
create only tag `v0.1.0-preview` at reviewed main, create a GitHub Pre-release,
and upload the approved ZIP and its SHA-256 companion. Verify remote tag,
asset sizes and download links. Until then, source publication can proceed;
this document does not claim that a binary Release exists.
