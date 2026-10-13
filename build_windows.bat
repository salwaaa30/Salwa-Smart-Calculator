@echo off
setlocal

cd /d "%~dp0"
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

python -m PyInstaller --onefile --windowed --clean --name "Salwa Smart Calculator" app.py
if errorlevel 1 exit /b 1

echo.
echo Build selesai: dist\Salwa Smart Calculator.exe
endlocal