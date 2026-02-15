@echo off
echo.
echo === Updating requirements.txt ===
echo.

call venv\Scripts\activate

REM Save current packages to requirements.txt
pip freeze > requirements.txt

echo.
echo requirements.txt has been updated with current packages.
echo.
echo Don't forget to commit and push:
echo   git add requirements.txt
echo   git commit -m "Updated requirements.txt"
echo   git push
echo.
pause