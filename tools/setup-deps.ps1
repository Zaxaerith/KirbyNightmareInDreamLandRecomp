$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$pin = Get-Content "$root/docs/FRAMEWORK_PIN.json" -Raw | ConvertFrom-Json
Push-Location $root
try {
    & git submodule update --init --recursive gbarecomp recomp-ui
    if ($LASTEXITCODE -ne 0) { throw 'Submodule initialization failed' }
    & git -C gbarecomp submodule update --init external/arm-recomp-core external/recomp-net external/rbengine
    if ($LASTEXITCODE -ne 0) { throw 'Framework dependency initialization failed' }
    if (-not (Test-Path '.deps/tomlplusplus/.git')) {
        & git init .deps/tomlplusplus
        if ($LASTEXITCODE -ne 0) { throw 'toml++ repository initialization failed' }
        & git -C .deps/tomlplusplus remote add origin $pin.tomlplusplus_repository
        if ($LASTEXITCODE -ne 0) { throw 'toml++ remote setup failed' }
    }
    & git -C .deps/tomlplusplus rev-parse --verify HEAD *> $null
    if ($LASTEXITCODE -ne 0) {
        if (& git -C .deps/tomlplusplus status --porcelain) { throw 'Unexpected files in incomplete toml++ checkout; preserve local changes' }
        & git -c http.version=HTTP/1.1 -c http.lowSpeedLimit=1024 -c http.lowSpeedTime=30 -C .deps/tomlplusplus fetch --depth 1 origin $pin.tomlplusplus_commit
        if ($LASTEXITCODE -ne 0) { throw 'toml++ pinned fetch failed; rerun after resolving network access' }
        & git -C .deps/tomlplusplus checkout --detach $pin.tomlplusplus_commit
        if ($LASTEXITCODE -ne 0) { throw 'toml++ checkout failed' }
    }
    foreach ($item in @(@('gbarecomp',$pin.commit), @('recomp-ui',$pin.recomp_ui_commit), @('.deps/tomlplusplus',$pin.tomlplusplus_commit))) {
        $head = & git -C $item[0] rev-parse HEAD
        if ($LASTEXITCODE -ne 0 -or $head -ne $item[1]) { throw "Pin mismatch: $($item[0]); preserve local changes" }
    }
    Write-Host 'PASS: pinned framework, recomp-ui and toml++'
} finally { Pop-Location }
