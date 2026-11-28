@echo off
chcp 65001 >nul
set "REPO_DIR=%~dp0"
set "PY=%REPO_DIR%..\VieNeu-TTS\.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo Chua cai VieNeu-TTS. Hay chay setup_all.bat truoc.
    pause
    exit /b 1
)
"%PY%" "%REPO_DIR%preview_voices.py" %*
pause
