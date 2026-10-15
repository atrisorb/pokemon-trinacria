# Pokémon Trinacria - builds F:\Progetti\pokeheartgold through WSL (Ubuntu, user atrisorb)
# and prints one verdict line: BUILD_OK or BUILD_FAILED.
# Usage (PowerShell):  & "F:\Progetti\pokeheartgold\tools\trinacria\build_trinacria.ps1"
# The repository path is pure ASCII, so no mirror is needed (unlike F:\Progetti\pokémon-trinacria).
$ErrorActionPreference = 'Continue'
$log = Join-Path $env:TEMP 'trinacria_build.log'
$cmd = 'cd /mnt/f/Progetti/pokeheartgold && ' +
       'export LM_LICENSE_FILE=/mnt/f/Progetti/pokeheartgold/tools/mwccarm/license.dat && ' +
       'export WSLENV="LM_LICENSE_FILE/p${WSLENV:+:$WSLENV}" && ' +
       'make -j6 WSL_ACCESSING_WINDOWS=0 rom; ' +
       'echo "make exit status: $?"; ' +
       'sha1sum build/pokeheartgold.us.nds 2>/dev/null'
wsl -d Ubuntu -u atrisorb -- bash -lc $cmd *> $log
$text = Get-Content $log -Raw
Write-Output "full log: $log"
$rom = ($text -split "`n" | Where-Object { $_ -match '^[0-9a-f]{40}\s+build/pokeheartgold\.us\.nds' } | Select-Object -First 1)
if ($text -match 'make exit status: 0') {
    Write-Output "ROM: $rom"
    Write-Output 'BUILD_OK'
    exit 0
}
Write-Output '--- last lines ---'
Get-Content $log -Tail 45
Write-Output 'BUILD_FAILED'
exit 1
