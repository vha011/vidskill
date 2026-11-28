@echo off
rem Dung: new-project.bat <skill> <slug> [--theme=<ten>]   |   new-project.bat <skill> --theme=list
rem Boc cho new-project.ps1, khong can Git Bash.
setlocal
set "SKILL=%~1"
set "SLUG="
set "THEME="
shift
:parse
if "%~1"=="" goto run
set "A=%~1"
if /i "%A:~0,8%"=="--theme=" (set "THEME=%A:~8%") else (set "SLUG=%~1")
shift
goto parse
:run
if "%SKILL%"=="" (
    echo Dung: new-project.bat ^<skill^> ^<slug^> [--theme=^<ten^>]
    exit /b 1
)
if defined THEME (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0new-project.ps1" "%SKILL%" "%SLUG%" -Theme "%THEME%"
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0new-project.ps1" "%SKILL%" "%SLUG%"
)
exit /b %ERRORLEVEL%
