@echo off
echo Creating desktop shortcut for Veterinary Clinic Management...

:: Get the current directory
set CURRENT_DIR=%~dp0
set EXE_PATH=%CURRENT_DIR%VeterinaryClinic.exe

:: Get the desktop path
set DESKTOP=%USERPROFILE%\Desktop

:: Create the shortcut
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Veterinary Clinic.lnk'); $Shortcut.TargetPath = '%EXE_PATH%'; $Shortcut.IconLocation = '%EXE_PATH%,0'; $Shortcut.Save()"

echo Shortcut created on the desktop.
echo.
echo You can now launch the application by double-clicking the "Veterinary Clinic" shortcut on your desktop.
pause 