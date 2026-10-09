param([int]$Frames = 720, [string]$Rom, [string]$Bios, [string]$Replay, [string]$Name = 'title', [switch]$Window, [string]$SavePath)
. "$PSScriptRoot\common.ps1"
if ($Frames -lt 1 -or $Frames -gt 12000) { throw 'Smoke frame bound is 1..12000 (bounded first-stage acceptance).' }
if ($Name -notmatch '^[a-zA-Z0-9_-]+$') { throw 'Use a simple log name.' }
if (-not $Rom) { $Rom = $DefaultRom }
if (-not $Bios) { $Bios = $DefaultBios }
Assert-Rom $Rom
Assert-Bios $Bios
New-Item -ItemType Directory -Force -Path "$ProjectRoot\logs" | Out-Null
if (-not $SavePath) { $SavePath = "$ProjectRoot\logs\$Name.sav" }
$SavePath = [IO.Path]::GetFullPath($SavePath)
if (-not $SavePath.StartsWith("$ProjectRoot\logs\", [StringComparison]::OrdinalIgnoreCase)) { throw 'Smoke saves must stay under project logs/.' }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $SavePath) | Out-Null
$oldReplay = $env:GBARECOMP_INPUT_REPLAY
$oldHeal = $env:GBARECOMP_SELFHEAL_RECOMPILE
$oldCoverage = $env:GBARECOMP_COVERAGE_JSON
$oldMisses = $env:GBARECOMP_MISS_FRAG
Push-Location $ProjectRoot
try {
    $env:GBARECOMP_SELFHEAL_RECOMPILE = '0'
    $env:GBARECOMP_INPUT_REPLAY = $null
    $env:GBARECOMP_COVERAGE_JSON = "$ProjectRoot\logs\$Name-coverage.json"
    $env:GBARECOMP_MISS_FRAG = "$ProjectRoot\logs\$Name-misses.toml.frag"
    if ($Replay) { $env:GBARECOMP_INPUT_REPLAY = (Resolve-Path -LiteralPath $Replay).Path }
    $mode = '--no-window'
    if ($Window) { $mode = '--window' }
    Invoke-Logged "$ProjectRoot\build\host\KirbyNightmareInDreamLandRecomp.exe" @('--rom',$Rom,'--bios',$Bios,"$ProjectRoot\game.toml",'--save',$SavePath,$mode,'--frames',"$Frames",'--dump-png',"$ProjectRoot\logs\$Name.png") "$ProjectRoot\logs\$Name.log"
    Get-Content -LiteralPath "$ProjectRoot\logs\$Name.log" -Tail 12
} finally {
    Pop-Location
    $env:GBARECOMP_INPUT_REPLAY = $oldReplay
    $env:GBARECOMP_SELFHEAL_RECOMPILE = $oldHeal
    $env:GBARECOMP_COVERAGE_JSON = $oldCoverage
    $env:GBARECOMP_MISS_FRAG = $oldMisses
}
