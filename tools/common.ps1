$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$DefaultRom = Join-Path $ProjectRoot 'Kirby - Nightmare in Dream Land (USA).gba'
$DefaultBios = Join-Path $ProjectRoot 'gba_bios.bin'
function Assert-Rom([string]$Path) {
    $bytes = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $Path).Path)
    if ($bytes.Length -ne 8388608 -or
        [Text.Encoding]::ASCII.GetString($bytes,0xA0,12).TrimEnd([char]0) -ne 'AGB KIRBY DX' -or
        [Text.Encoding]::ASCII.GetString($bytes,0xAC,4) -ne 'A7KE' -or $bytes[0xBC] -ne 0 -or
        (Get-FileHash -LiteralPath $Path -Algorithm SHA1).Hash -ne '37a476567d133c146fee6b5e2eb0b07a215da6b0') {
        throw 'Expected Kirby USA A7KE Rev 0 ROM, SHA1 37a476567d133c146fee6b5e2eb0b07a215da6b0.'
    }
}
function Assert-Bios([string]$Path) {
    if ((Get-Item -LiteralPath $Path).Length -ne 16384 -or
        (Get-FileHash -LiteralPath $Path -Algorithm SHA1).Hash -ne '300c20df6731a33952ded8c436f7f186d25d3492') {
        throw 'Expected user-supplied 16 KiB GBA BIOS, SHA1 300c20df6731a33952ded8c436f7f186d25d3492.'
    }
}
function Invoke-Logged([string]$Program, [string[]]$Arguments, [string]$Log) {
    $ErrorActionPreference = 'Continue'
    & $Program @Arguments *> $Log
    $code = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    if ($code -ne 0) { Get-Content -LiteralPath $Log -Tail 35; throw "$Program exited $code; see $Log" }
}
