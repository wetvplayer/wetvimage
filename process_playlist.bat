@echo off
chcp 65001 >nul
title IPTV All-in-One Playlist Automation

echo ===================================================================
echo   IPTV ALL-IN-ONE AUTOMATION (Logos + GitHub CDN + MCP Upload)
echo ===================================================================
echo.

set M3U_INPUT=%~1
if "%M3U_INPUT%"=="" set M3U_INPUT=all kurdish.m3u

set CATEGORY=%~2
if "%CATEGORY%"=="" set CATEGORY=Kurdish TV

set BOUQUET=%~3
if "%BOUQUET%"=="" set BOUQUET=Kurdish Channels

set LINE=%~4
if "%LINE%"=="" set LINE=123

echo Processing Playlist: "%M3U_INPUT%"
echo Category:            "%CATEGORY%"
echo Bouquet:             "%BOUQUET%"
echo Line Account:        "%LINE%"
echo.

py scripts\process_all_in_one.py "%M3U_INPUT%" --category "%CATEGORY%" --bouquet "%BOUQUET%" --line "%LINE%"

echo.
echo ===================================================================
echo   Process Finished! Press any key to exit...
echo ===================================================================
pause >nul
