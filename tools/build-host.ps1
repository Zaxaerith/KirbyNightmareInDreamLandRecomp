param([int]$Jobs = 4, [Parameter(Mandatory=$true)][string]$Toolchain,
      [Parameter(Mandatory=$true)][string]$SdlRoot, [switch]$GeneratorOnly)
. "$PSScriptRoot\common.ps1"
if ($Jobs -lt 1) { throw 'Jobs must be positive.' }
$sdl = (Resolve-Path -LiteralPath $SdlRoot).Path.Replace('\','/')
New-Item -ItemType Directory -Force -Path "$ProjectRoot\logs" | Out-Null
$argsConfigure = @('-S',$ProjectRoot,'-B',"$ProjectRoot\build\host",'-G','Ninja','-DCMAKE_BUILD_TYPE=Release',
    "-DCMAKE_C_COMPILER=$Toolchain/bin/gcc.exe","-DCMAKE_CXX_COMPILER=$Toolchain/bin/g++.exe",
    "-DSDL2_INCLUDE_DIR=$sdl/include/SDL2","-DSDL2_LIBRARY=$sdl/lib/libSDL2.dll.a","-DSDL2_DLL=$sdl/bin/SDL2.dll",
    "-DGBARECOMP_MINGW_RUNTIME_BIN=$Toolchain/bin",
    "-DGBARECOMP_ROOT=$ProjectRoot/gbarecomp","-DGBARECOMP_TOMLPP_INCLUDE_DIR=$ProjectRoot/.deps/tomlplusplus",
    "-DRECOMP_UI_ROOT=$ProjectRoot/recomp-ui")
Invoke-Logged 'cmake' $argsConfigure "$ProjectRoot\logs\host-configure.log"
$target = 'KirbyNightmareInDreamLandRecomp'
if ($GeneratorOnly) { $target = 'gba_recompile' }
Invoke-Logged 'cmake' @('--build',"$ProjectRoot\build\host",'--target',$target,'--parallel',"$Jobs") "$ProjectRoot\logs\host-build.log"
if (-not $GeneratorOnly) { Get-Item -LiteralPath "$ProjectRoot\build\host\KirbyNightmareInDreamLandRecomp.exe" | Select-Object FullName,Length }
