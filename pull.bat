@echo off
echo.
echo === Getting Latest Changes ===
echo.

REM Pull from GitHub
git pull

echo.
echo === Activating Virtual Environment ===
echo.

REM Activate virtual environment
call venv\Scripts\activate

echo.
echo === Checking for New Packages ===
echo.

REM Install any new packages from requirements.txt
pip install -r requirements.txt --quiet

echo.
echo === Ready! ===
echo.
echo Virtual environment is active.
echo All packages are up to date.
echo.
echo You can now run: python app.py
echo.

REM Keep command prompt open with venv activated
cmd /k