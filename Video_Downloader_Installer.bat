@echo off
echo ==========================================
echo    Video Downloader - Installation
echo ==========================================
echo.
echo Installing Video Downloader...
echo This will automatically set up everything you need.
echo.

REM Create installation directory
set "INSTALL_DIR=%USERPROFILE%\VideoDownloader"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [1/4] Copying application files...
copy "VideoDownloader.exe" "%INSTALL_DIR%\" >nul

echo [2/4] Creating desktop shortcut...
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\Video Downloader.lnk"

REM Create VBScript to make shortcut
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%SHORTCUT%"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "%INSTALL_DIR%\VideoDownloader.exe"
echo oLink.WorkingDirectory = "%INSTALL_DIR%"
echo oLink.Description = "Video Downloader - Download videos and audio from the web"
echo oLink.Save
) > temp_shortcut.vbs
cscript //nologo temp_shortcut.vbs
del temp_shortcut.vbs

echo [3/4] Creating start menu entry...
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
copy "%DESKTOP%\Video Downloader.lnk" "%STARTMENU%\" >nul 2>&1

echo [4/4] Finalizing installation...
echo.
echo ✅ Installation completed successfully!
echo.
echo Video Downloader has been installed to: %INSTALL_DIR%
echo.
echo You can now:
echo • Use the desktop shortcut to launch the application
echo • Find it in your Start Menu
echo • Download videos and convert audio to MP3 automatically
echo.
echo Press any key to launch Video Downloader now...
pause >nul

start "" "%INSTALL_DIR%\VideoDownloader.exe"

exit /b 0