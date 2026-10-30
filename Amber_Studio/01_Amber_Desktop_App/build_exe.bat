@echo off
setlocal
cd /d "%~dp0"
echo === Building AmberStudio (AmberStudioSetup.exe = one file to share) ===
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
if errorlevel 1 goto fail

rem clean old builds so no stale files are left behind (AmberStudio.spec is kept)
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

rem --onedir = no unpacking on every launch, so AmberStudio opens much faster.
rem --specpath build keeps PyInstaller from overwriting AmberStudio.spec in this folder.
rem The icon path is absolute because --specpath makes relative paths resolve from the build folder.
python -m PyInstaller --noconfirm --clean --onedir --noconsole --name AmberStudio --distpath "%~dp0build\app" --specpath build --icon "%~dp0amber.ico" --collect-all yt_dlp --collect-all imageio_ffmpeg --collect-all webview --collect-all pythonnet --collect-all clr_loader --collect-all mutagen --collect-all yt_dlp_ejs --add-data "%~dp0vendor;vendor" amber_studio.py
if errorlevel 1 goto fail

echo.
echo === App files built (internal step, in build\app) ===

rem ---- Find Inno Setup (free); try to install it with winget if it is missing ----
call :findinno
if defined ISCC goto haveinno
echo.
echo Inno Setup 6 not found. Trying to install it with winget (accept the Windows prompt if it appears)...
winget install -e --id JRSoftware.InnoSetup --silent --accept-package-agreements --accept-source-agreements
call :findinno
if not defined ISCC goto noinno

:haveinno
echo Building installer with Inno Setup...
"%ISCC%" AmberStudio.iss
if errorlevel 1 goto fail
echo.
echo === Done. dist\AmberStudioSetup.exe is the ONLY file in dist. Share just that one. ===
echo It asks where to install, then adds a Desktop shortcut and a Start menu entry.
pause
exit /b 0

:noinno
echo.
echo === Inno Setup 6 was not found, so AmberStudioSetup.exe was NOT made. ===
echo Install it once (free), then run build_exe.bat again:
echo    winget install -e --id JRSoftware.InnoSetup
echo    or download from https://jrsoftware.org/isdl.php
echo No single-file exe can be made without it (the app itself is a folder: build\app\AmberStudio).
pause
exit /b 1

:fail
echo.
echo === Build failed. Check the messages above. ===
pause
exit /b 1

:findinno
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
exit /b 0
