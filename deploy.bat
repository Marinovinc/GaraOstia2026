@echo off
REM ============================================================
REM  deploy.bat - doppio-click per pubblicare l'app sul telefono
REM  Rigenera lo snapshot del giorno e lo mette online (GitHub).
REM  Doppio-click = data di ieri (con fallback). Per una data:
REM    apri il prompt qui e scrivi:  deploy.bat 2026-06-25
REM ============================================================
cd /d "D:\Dev\IschiaFishing"
echo.
echo  Pubblicazione app gara Ostia su GitHub Pages...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "deploy.ps1" %*
echo.
pause
