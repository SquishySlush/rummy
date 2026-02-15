@echo off
echo.
echo === Saving Changes to Git ===
echo.

REM Add all changes
git add .

REM Ask for commit message
set /p message="Enter commit message: "

REM Commit with message
git commit -m "%message%"

REM Push to GitHub
git push

echo.
echo === Done! ===
echo.
pause