@echo off
chcp 65001 >nul
echo =======================================================================
echo    EXPLAINED VIDEO ENGINE - TU DONG CAI DAT TOAN BO
echo    (herk-edit-kit + VieNeu-TTS + Skills + Offline AI Engine)
echo =======================================================================
echo.

:: Repo nay (vidskill) la thu muc lam viec. herk-edit-kit va VieNeu-TTS duoc clone
:: vao thu muc CHA, cung cap voi repo (dung nhu AGENTS.md mo ta).
set "REPO_DIR=%~dp0"
if "%REPO_DIR:~-1%"=="\" set "REPO_DIR=%REPO_DIR:~0,-1%"
set "INSTALL_DIR=%REPO_DIR%\.."
cd /d "%INSTALL_DIR%"
echo Repo (vidskill):      %REPO_DIR%
echo Thu muc cai dat goc:  %CD%
echo.

:: -------------------------------------------------------------------------
:: BUOC 1: KIEM TRA / TU CAI Git, Node, Python, FFmpeg (qua winget neu thieu)
:: -------------------------------------------------------------------------
echo [1/5] Kiem tra cac cong cu he thong...

set "HAS_WINGET="
where winget >nul 2>&1 && set "HAS_WINGET=1"

where git >nul 2>&1
if %ERRORLEVEL% neq 0 if defined HAS_WINGET (
    echo   -> Chua co Git, dang tu cai bang winget...
    winget install -e --id Git.Git --silent --accept-package-agreements --accept-source-agreements
    set "PATH=%PATH%;C:\Program Files\Git\cmd"
)
where git >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LOI] Khong cai duoc Git! Cai tay tai https://git-scm.com/ roi chay lai.
    pause
    exit /b 1
)
echo   [OK] Git san sang.

where node >nul 2>&1
if %ERRORLEVEL% neq 0 if defined HAS_WINGET (
    echo   -> Chua co Node.js, dang tu cai ban LTS bang winget...
    winget install -e --id OpenJS.NodeJS.LTS --silent --accept-package-agreements --accept-source-agreements
    set "PATH=%PATH%;C:\Program Files\nodejs"
)
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LOI] Khong cai duoc Node.js! Cai tay ban LTS ^>= 22 tai https://nodejs.org/ roi chay lai.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('node -v') do echo   [OK] Node.js %%v san sang.

where python >nul 2>&1
if %ERRORLEVEL% neq 0 if defined HAS_WINGET (
    echo   -> Chua co Python, dang tu cai Python 3.12 bang winget...
    winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    for /d %%d in ("%LOCALAPPDATA%\Programs\Python\Python312*") do set "PATH=%%d;%%d\Scripts;%PATH%"
)
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LOI] Khong cai duoc Python! Cai tay Python 3.10-3.12 tai https://python.org/ ^(tick "Add to PATH"^) roi chay lai.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do echo   [OK] %%v san sang.

where ffmpeg >nul 2>&1
if %ERRORLEVEL% neq 0 if defined HAS_WINGET (
    echo   -> Chua co FFmpeg, dang tu cai bang winget...
    winget install -e --id Gyan.FFmpeg --silent --accept-package-agreements --accept-source-agreements
)
where ffmpeg >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [CANH BAO] FFmpeg chua co trong PATH ^(co the can mo lai cua so CMD sau khi cai^).
) else (
    echo   [OK] FFmpeg san sang.
)

:: -------------------------------------------------------------------------
:: BUOC 2: herk-edit-kit (HyperFrames + GSAP)
:: -------------------------------------------------------------------------
echo.
if not exist "output" mkdir "output"
echo [2/5] Cai dat herk-edit-kit (Render Engine)...
if not exist "herk-edit-kit" (
    echo   -> git clone herk-edit-kit...
    git clone https://github.com/nateherkai/herk-edit-kit.git
    if %ERRORLEVEL% neq 0 (
        echo [LOI] Khong the clone herk-edit-kit. Kiem tra mang!
        pause
        exit /b 1
    )
) else (
    echo   -> herk-edit-kit da ton tai, dang cap nhat...
    git -C herk-edit-kit pull
)
echo   -> npm install...
pushd herk-edit-kit
call npm install
popd
echo   [OK] herk-edit-kit xong.

:: -------------------------------------------------------------------------
:: BUOC 3: VieNeu-TTS (giong doc AI tieng Viet)
:: -------------------------------------------------------------------------
echo.
echo [3/5] Cai dat VieNeu-TTS (giong doc AI Offline)...
if not exist "VieNeu-TTS" (
    echo   -> git clone VieNeu-TTS...
    git clone https://github.com/pnnbao97/VieNeu-TTS.git
    if %ERRORLEVEL% neq 0 (
        echo [LOI] Khong the clone VieNeu-TTS. Kiem tra mang!
        pause
        exit /b 1
    )
) else (
    echo   -> VieNeu-TTS da ton tai, dang cap nhat...
    git -C VieNeu-TTS pull
)

pushd VieNeu-TTS
if not exist ".venv" python -m venv .venv
".venv\Scripts\python.exe" -m pip install --upgrade pip
echo   -> Dang cai dependencies cho VieNeu-TTS (co the mat vai phut)...
".venv\Scripts\python.exe" -m pip install torch torchaudio transformers onnxruntime soundfile soxr kaldi-native-fbank tokenizers sea-g2p huggingface_hub pillow requests beautifulsoup4
".venv\Scripts\python.exe" -m pip install -e .
popd
echo   [OK] VieNeu-TTS xong.

:: -------------------------------------------------------------------------
:: BUOC 4: Model offline (neu co)
:: -------------------------------------------------------------------------
echo.
echo [4/5] Cau hinh model giong Truc Ly (v3 Turbo)...
set "OFFLINE_MODEL_SRC=%REPO_DIR%\models_offline\models--pnnbao-ump--VieNeu-TTS-v3-Turbo"
set "HF_HUB_CACHE=%USERPROFILE%\.cache\huggingface\hub\models--pnnbao-ump--VieNeu-TTS-v3-Turbo"

if exist "%OFFLINE_MODEL_SRC%" (
    if not exist "%HF_HUB_CACHE%" (
        echo   -> Nap model offline vao cache may...
        robocopy "%OFFLINE_MODEL_SRC%" "%HF_HUB_CACHE%" /E /NFL /NDL /NJH /NJS /R:1 /W:1 >nul
        echo   [OK] Da nap model offline.
    ) else (
        echo   [OK] Model da co san trong cache.
    )
) else (
    echo   [INFO] Khong co models_offline. Model se tu tai ve o lan chay dau tien.
)

:: -------------------------------------------------------------------------
:: BUOC 5: Dang ky Skill cho AI Agent
:: -------------------------------------------------------------------------
echo.
echo [5/5] Dang ky Agent Skill 'explained-video-maker'...
if exist "%REPO_DIR%\SKILL.md" (
    set "GEMINI_SKILL_DIR=%USERPROFILE%\.gemini\config\skills\explained-video-maker"
    mkdir "%USERPROFILE%\.gemini\config\skills\explained-video-maker" 2>nul
    copy /Y "%REPO_DIR%\SKILL.md" "%USERPROFILE%\.gemini\config\skills\explained-video-maker\SKILL.md" >nul
    mkdir "%USERPROFILE%\.claude\skills\explained-video-maker" 2>nul
    copy /Y "%REPO_DIR%\SKILL.md" "%USERPROFILE%\.claude\skills\explained-video-maker\SKILL.md" >nul
    echo   [OK] Da dang ky skill cho Antigravity/Gemini va Claude Code.
)

echo.
echo Kiem tra nhanh HyperFrames...
pushd herk-edit-kit
call npx --no-install hyperframes --help >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo   [CANH BAO] Chua goi duoc hyperframes. Chay lai: cd herk-edit-kit ^&^& npm install
) else (
    echo   [OK] hyperframes san sang.
)
popd

echo.
echo =======================================================================
echo    CAI DAT HOAN TAT
echo    - herk-edit-kit : %INSTALL_DIR%\herk-edit-kit
echo    - VieNeu-TTS    : %INSTALL_DIR%\VieNeu-TTS
echo    - Chon giong doc: chay preview_voices.bat ^(nghe thu va chon^)
echo    - Buoc tiep: mo AI Agent tai %REPO_DIR% va bao no doc AGENTS.md
echo =======================================================================
echo.
pause
