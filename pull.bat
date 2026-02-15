@echo off
echo.
echo === Syncing Project ===
echo.

git pull

call venv\Scripts\activate

REM Only install if requirements.txt changed
git diff HEAD@{1} HEAD --name-only | findstr /C:"requirements.txt" >nul
if %errorlevel% equ 0 (
    pip install -r requirements.txt
)

echo.
echo === Ready! ===
echo.

cmd /k