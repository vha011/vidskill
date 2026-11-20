@echo off
chcp 65001 >nul
echo =======================================================================
echo    EXPLAINED VIDEO ENGINE — TỰ ĐỘNG CÀI ĐẶT TOÀN BỘ REPOSITORIES
echo    (herk-edit-kit + VieNeu-TTS + Motion Skills + Offline AI Engine)
echo =======================================================================
echo.

set "INSTALL_DIR=%~dp0.."
cd /d "%INSTALL_DIR%"
echo Thư mục cài đặt gốc: %CD%
echo.

:: -------------------------------------------------------------------------
:: BƯỚC 1: KIỂM TRA ĐIỀU KIỆN TIÊN QUYẾT (Git, Node, Python, FFmpeg)
:: -------------------------------------------------------------------------
echo [1/5] Kiểm tra các công cụ hệ thống...

where git >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LỖI] Chưa cài đặt Git! Vui lòng cài Git tại https://git-scm.com/
    pause
    exit /b 1
)
echo   [OK] Git đã sẵn sàng.

where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LỖI] Chưa cài đặt Node.js! Vui lòng cài Node.js LTS (>= 22.x) tại https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('node -v') do echo   [OK] Node.js %%v đã sẵn sàng.

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LỖI] Chưa cài đặt Python! Vui lòng cài Python 3.10-3.12 tại https://python.org/ (nhớ tick "Add to PATH").
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do echo   [OK] Python %%v đã sẵn sàng.

where ffmpeg >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [CẢNH BÁO] Chưa tìm thấy FFmpeg trong PATH!
    echo            Khuyên dùng: mở PowerShell gõ 'winget install Gyan.FFmpeg' để tự cài đặt.
) else (
    echo   [OK] FFmpeg đã sẵn sàng.
)

:: -------------------------------------------------------------------------
:: BƯỚC 2: CLONE VÀ CÀI ĐẶT HERK-EDIT-KIT (HyperFrames + GSAP + 400+ Motion Cards)
:: -------------------------------------------------------------------------
echo.
echo [2/5] Cài đặt Repo herk-edit-kit (Motion Graphics & Video Editing Engine)...
if not exist "herk-edit-kit" (
    echo   -> Đang git clone herk-edit-kit từ GitHub...
    git clone https://github.com/nateherkai/herk-edit-kit.git
    if %ERRORLEVEL% neq 0 (
        echo [LỖI] Không thể clone herk-edit-kit. Vui lòng kiểm tra kết nối mạng!
        pause
        exit /b 1
    )
) else (
    echo   -> Thư mục herk-edit-kit đã tồn tại. Đang cập nhật...
    cd herk-edit-kit
    git pull
    cd ..
)

echo   -> Đang cài đặt thư viện Node.js cho herk-edit-kit (npm install)...
cd herk-edit-kit
call npm install
cd ..
echo   [OK] herk-edit-kit đã được cài đặt hoàn tất.

:: -------------------------------------------------------------------------
:: BƯỚC 3: CLONE VÀ CÀI ĐẶT VIENEU-TTS (Vietnamese Voice AI)
:: -------------------------------------------------------------------------
echo.
echo [3/5] Cài đặt Repo VieNeu-TTS (Giọng đọc AI tiếng Việt Offline)...
if not exist "VieNeu-TTS" (
    echo   -> Đang git clone VieNeu-TTS từ GitHub...
    git clone https://github.com/pnnbao97/VieNeu-TTS.git
    if %ERRORLEVEL% neq 0 (
        echo [LỖI] Không thể clone VieNeu-TTS. Vui lòng kiểm tra kết nối mạng!
        pause
        exit /b 1
    )
) else (
    echo   -> Thư mục VieNeu-TTS đã tồn tại. Đang cập nhật...
    cd VieNeu-TTS
    git pull
    cd ..
)

echo   -> Đang tạo môi trường ảo Python (.venv) cho VieNeu-TTS...
cd VieNeu-TTS
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
echo   -> Đang cài đặt dependencies cho VieNeu-TTS...
python -m pip install torch torchaudio transformers onnxruntime soundfile soxr kaldi-native-fbank tokenizers sea-g2p huggingface_hub pillow requests beautifulsoup4
python -m pip install -e .
call deactivate
cd ..
echo   [OK] VieNeu-TTS đã được cấu hình hoàn tất.

:: -------------------------------------------------------------------------
:: BƯỚC 4: NẠP MODEL OFFLINE NẾU CÓ SẴN TRONG BỘ CÀI
:: -------------------------------------------------------------------------
echo.
echo [4/5] Cấu hình Model AI Trúc Ly (v3 Turbo)...
set "OFFLINE_MODEL_SRC=%INSTALL_DIR%\juno-ugc-toolkit\models_offline\models--pnnbao-ump--VieNeu-TTS-v3-Turbo"
set "HF_HUB_CACHE=%USERPROFILE%\.cache\huggingface\hub\models--pnnbao-ump--VieNeu-TTS-v3-Turbo"

if exist "%OFFLINE_MODEL_SRC%" (
    if not exist "%HF_HUB_CACHE%" (
        echo   -> Phát hiện model offline trong bộ cài. Đang nạp vào cache máy...
        robocopy "%OFFLINE_MODEL_SRC%" "%HF_HUB_CACHE%" /E /NFL /NDL /NJH /NJS /R:1 /W:1 >nul
        echo   [OK] Đã nạp thành công 794 MB model offline.
    ) else (
        echo   [OK] Model VieNeu-TTS v3 Turbo đã có sẵn trong cache máy.
    )
) else (
    echo   [THÔNG BÁO] Không có sẵn thư mục models_offline.
    echo   VieNeu-TTS sẽ tự động tải model về khi chạy lần đầu tiên.
)

:: -------------------------------------------------------------------------
:: BƯỚC 5: ĐĂNG KÝ SKILL CHO AI AGENT (Antigravity & Claude Code)
:: -------------------------------------------------------------------------
echo.
echo [5/5] Đăng ký Agent Skill 'explained-video-maker' cho AI...
set "GEMINI_SKILL_DIR=%USERPROFILE%\.gemini\config\skills\explained-video-maker"
if not exist "%GEMINI_SKILL_DIR%" (
    mkdir "%GEMINI_SKILL_DIR%" 2>nul
)
if exist "%INSTALL_DIR%\SETUP-NEW-MACHINE\SKILL.md" (
    copy /Y "%INSTALL_DIR%\SETUP-NEW-MACHINE\SKILL.md" "%GEMINI_SKILL_DIR%\SKILL.md" >nul
    echo   [OK] Đã cài đặt Skill vào Antigravity IDE: %GEMINI_SKILL_DIR%
)

echo.
echo =======================================================================
echo    🎉 TẤT CẢ REPOSITORIES & MÔI TRƯỜNG ĐÃ ĐƯỢC THIẾT LẬP THÀNH CÔNG!
echo    - herk-edit-kit: Sẵn sàng làm motion graphics (400+ card styles)
echo    - VieNeu-TTS:    Sẵn sàng sinh giọng đọc Trúc Ly offline
echo    - Agent Skill:   Đã đăng ký 'explained-video-maker'
echo =======================================================================
echo.
pause
