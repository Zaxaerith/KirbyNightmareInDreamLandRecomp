param([string]$Version = '0.1.0-preview', [Parameter(Mandatory=$true)][string]$Toolchain,
      [Parameter(Mandatory=$true)][string]$SdlRoot,
      [string]$Python = 'python', [switch]$SkipBuild)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
if ($Version -notmatch '^\d+\.\d+\.\d+(-[a-z0-9.-]+)?$') { throw 'Invalid version' }
$SdlRoot = (Resolve-Path -LiteralPath $SdlRoot).Path
$pin = Get-Content "$root/docs/FRAMEWORK_PIN.json" -Raw | ConvertFrom-Json
foreach ($pair in @(@('gbarecomp',$pin.commit),@('recomp-ui',$pin.recomp_ui_commit),@('.deps/tomlplusplus',$pin.tomlplusplus_commit))) {
    $head = & git -C "$root/$($pair[0])" rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $pair[1]) { throw "Dependency pin mismatch: $($pair[0])" }
    $status = & git -C "$root/$($pair[0])" status --porcelain --untracked-files=no
    if ($LASTEXITCODE -ne 0 -or $status) { throw "Modified dependency: $($pair[0])" }
}
if (-not $SkipBuild) { & "$PSScriptRoot/build-host.ps1" -Toolchain $Toolchain -SdlRoot $SdlRoot }
if (-not (Select-String -LiteralPath "$root/build/host/CMakeCache.txt" -Pattern '^CMAKE_BUILD_TYPE:STRING=Release$')) { throw 'Release build required' }
$name = "KirbyNightmareInDreamLandRecomp-windows-x64-v$Version"
$stage = "$root/release-stage/$name"
$zip = "$stage.zip"
if ((Test-Path -LiteralPath $stage) -or (Test-Path -LiteralPath $zip) -or (Test-Path -LiteralPath "$zip.sha256")) { throw 'Candidate output already exists; preserve it or select another version' }
New-Item -ItemType Directory -Path "$stage/licenses/mpl-source" -Force | Out-Null
$binaries = @('KirbyNightmareInDreamLandRecomp.exe','SDL2.dll','libgcc_s_seh-1.dll','libstdc++-6.dll','libwinpthread-1.dll')
foreach ($file in $binaries) {
    Copy-Item -LiteralPath "$root/build/host/$file" -Destination "$stage/$file"
    & "$Toolchain/bin/strip.exe" --strip-debug "$stage/$file"
    if ($LASTEXITCODE -ne 0) { throw "Strip failed: $file" }
}
# Asset allowlist is shared with the audit; no recursive copying from a dirty build.
$assets = @('fonts/LatoLatin-Regular.ttf','fonts/LatoLatin-Bold.ttf','fonts/OpenMoji-black-glyf.ttf','fonts/NotoSansSymbols2-Regular.ttf',
    'img/brand_mark.tga','img/verdict_ok.tga','img/verdict_warn.tga','img/verdict_bad.tga','img/verdict_none.tga','img/flags.png','img/pad_gba.tga')
foreach ($asset in $assets) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent "$stage/assets/$asset") | Out-Null
    Copy-Item -LiteralPath "$root/build/host/assets/$asset" -Destination "$stage/assets/$asset"
}
foreach ($doc in @('LICENSE.md','THIRD_PARTY_NOTICES.md')) { Copy-Item -LiteralPath "$root/$doc" -Destination "$stage/$doc" }
# Include the exact original-code terms without adding an unreviewed package file.
$licenseScope = Get-Content -LiteralPath "$root/LICENSE.md" -Raw
$licenseTerms = Get-Content -LiteralPath "$root/LICENSE" -Raw
"$licenseScope`n`n---`n`n## Full original-code license terms`n`n$licenseTerms" | Set-Content -LiteralPath "$stage/LICENSE.md" -Encoding utf8
Copy-Item -LiteralPath "$root/recomp/player-README.md" -Destination "$stage/README.md"
$licenses = @{
    'GBARecomp'="$root/gbarecomp/LICENSE"; 'RecompUI'="$root/recomp-ui/LICENSE";
    'ImGui'="$root/recomp-ui/src/third_party/imgui/LICENSE.txt"; 'ArmRecompCore'="$root/gbarecomp/external/arm-recomp-core/LICENSE";
    'RecompNet'="$root/gbarecomp/external/recomp-net/LICENSE"; 'Rbengine'="$root/gbarecomp/external/rbengine/LICENSE";
    'SDL2'="$(Split-Path -Parent $SdlRoot)/LICENSE.txt"; 'GCC-GPL3'="$Toolchain/licenses/gcc/COPYING3";
    'GCC-LGPL3'="$Toolchain/licenses/gcc/COPYING3.LIB"; 'GCC-Runtime-Exception'="$Toolchain/licenses/gcc/COPYING.RUNTIME";
    'MinGW-Runtime'="$Toolchain/licenses/mingw-w64/COPYING.MinGW-w64-runtime.txt";
    'Font-Notices'="$root/recomp-ui/assets/common/fonts/NOTICE.md"; 'Image-Notices'="$root/recomp-ui/assets/common/img/NOTICE.md";
    'MPL-2.0'="$root/gbarecomp/third_party/MPL-2.0.txt"; 'Framework-Attribution'="$root/gbarecomp/THIRD_PARTY_ATTRIBUTION.md";
    'TomlPlusPlus'="$root/.deps/tomlplusplus/LICENSE"
}
foreach ($key in $licenses.Keys) { Copy-Item -LiteralPath $licenses[$key] -Destination "$stage/licenses/$key.txt" }
foreach ($file in @('Lato-OFL','NotoSymbols-OFL','OpenMoji-LICENSE','JRickey-MIT','Reference-Integration')) {
    Copy-Item -LiteralPath "$root/docs/licenses/$file.txt" -Destination "$stage/licenses/$file.txt"
}
foreach ($file in @('bios_hle.cpp','bios_hle.h')) { Copy-Item -LiteralPath "$root/gbarecomp/src/runtime/$file" -Destination "$stage/licenses/mpl-source/$file" }
$manifest = @(Get-ChildItem -LiteralPath $stage -Recurse -File | Sort-Object FullName | ForEach-Object {
    [pscustomobject]@{file=$_.FullName.Substring($stage.Length+1).Replace('\','/'); bytes=$_.Length; sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
})
$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath "$stage/manifest.json" -Encoding utf8
& $Python "$PSScriptRoot/audit-release.py" $stage
if ($LASTEXITCODE -ne 0) { throw 'Stage audit failed' }
Compress-Archive -Path "$stage/*" -DestinationPath $zip -CompressionLevel Optimal
& $Python "$PSScriptRoot/audit-release.py" $zip
if ($LASTEXITCODE -ne 0) { throw 'ZIP audit failed' }
$hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
"$hash  $name.zip" | Set-Content -LiteralPath "$zip.sha256" -Encoding ascii
Write-Host "PASS: local candidate $zip"
Write-Host "SHA-256: $hash"
