@echo off
title Pushing Smart Hostel Mess Management System to GitHub
cd /d "C:\Smart-Hostel-Mess"
echo ======================================================================
echo   Pushing Smart Hostel Mess Management System to GitHub...
echo   Repo: https://github.com/khatalprachi9-lab/Smart-Hostel-Mess-Management-System
echo ======================================================================
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ======================================================================
    echo   SUCCESS! All project files have been successfully pushed to GitHub!
    echo ======================================================================
) else (
    echo ======================================================================
    echo   If prompted, please complete the browser sign-in or paste a GitHub Token.
    echo ======================================================================
)
pause

