@echo off
REM ========================================
REM Script para generar ADA en modo ONEDIR
REM (Inicio más rápido ~2-3 segundos)
REM ========================================

echo ========================================
echo Generando ADA en modo ONEDIR (RAPIDO)
echo ========================================
echo.

pyinstaller --onedir --windowed --name="ADA_PilotoAuto_v5_Fast" --icon="VicTor.ico" --add-data="VicTor.ico;." --add-data="credentials_gebilo.json;." --add-data="sucursales_history.py;." --hidden-import=ttkbootstrap --hidden-import=babel.numbers --hidden-import=gspread --hidden-import=google.oauth2.service_account --hidden-import=googleapiclient.discovery --collect-all ttkbootstrap "ADA - Piloto Auto v5.py"

echo.
echo ========================================
echo COMPLETADO!
echo ========================================
echo.
echo El ejecutable esta en: dist\ADA_PilotoAuto_v5_Fast\ADA_PilotoAuto_v5_Fast.exe
echo.
echo NOTA: Ahora tienes una CARPETA con varios archivos.
echo      Para distribuir, comprime toda la carpeta en ZIP.
echo.
echo VENTAJA: Inicio MUCHO mas rapido (2-3 segundos)
echo ========================================
pause
