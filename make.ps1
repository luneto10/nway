# PowerShell script to run make with MinGW in PATH
$env:Path += ";C:\MinGW\bin"
& "C:\MinGW\bin\make.exe" $args

