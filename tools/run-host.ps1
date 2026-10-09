param([string]$Rom, [string]$Bios, [string]$SavePath)
. "$PSScriptRoot\common.ps1"
if (-not $Rom) { $Rom = $DefaultRom }
if (-not $Bios) { $Bios = $DefaultBios }
Assert-Rom $Rom
Assert-Bios $Bios
if (-not $SavePath) { $SavePath = "$ProjectRoot\saves\kirby_nightmare_usa.sav" }
$SavePath = [IO.Path]::GetFullPath($SavePath)
if (-not $SavePath.StartsWith("$ProjectRoot\", [StringComparison]::OrdinalIgnoreCase)) { throw 'Save path must stay inside this project.' }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $SavePath) | Out-Null
Push-Location $ProjectRoot
try {
    & "$ProjectRoot\build\host\KirbyNightmareInDreamLandRecomp.exe" --rom $Rom --bios $Bios "$ProjectRoot\game.toml" --save $SavePath --window
    if ($LASTEXITCODE -ne 0) { throw "Host exited $LASTEXITCODE" }
} finally { Pop-Location }
