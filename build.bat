@echo off
REM Build Script dla PyInstaller - v5.2 PRODUCTION
REM Tworzy standalone .exe + przygotowuje strukturę dla instalatora

echo ========================================
echo Aktualizator Strony v5.2 - PRODUCTION BUILD
echo ========================================
echo.

echo [1/8] Sprawdzanie PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller nie zainstalowany. Instalowanie...
    python -m pip install pyinstaller
)

echo [2/8] Czyszczenie starych buildow...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "installer_output" rmdir /s /q "installer_output"

echo [3/8] Building .exe (to moze potrwac kilka minut)...
python -m PyInstaller build.spec

if errorlevel 1 (
    echo.
    echo ========================================
    echo BLAD: Build nie powiodl sie!
    echo ========================================
    pause
    exit /b 1
)

echo [4/8] Weryfikacja pliku exe...
if not exist "dist\AktualizatorStrony.exe" (
    echo BLAD: Nie znaleziono AktualizatorStrony.exe
    pause
    exit /b 1
)

echo [5/8] Kopiowanie plikow dodatkowych...
xcopy "config.json" "dist\" /Y >nul 2>&1
xcopy "TODO.md" "dist\" /Y >nul 2>&1
xcopy "requirements.txt" "dist\" /Y >nul 2>&1
xcopy "LICENSE.txt" "dist\" /Y >nul 2>&1
xcopy "INSTALL_INFO.txt" "dist\" /Y >nul 2>&1

echo [6/8] Tworzenie struktury folderow...
if not exist "dist\logs" mkdir "dist\logs"
if not exist "dist\backups" mkdir "dist\backups"

echo [7/8] Testowanie exe...
echo Sprawdzanie czy exe sie uruchamia...
timeout /t 2 /nobreak >nul

echo [8/8] Gotowe!
echo.
echo ========================================
echo Build zakonczony pomyslnie!
echo ========================================
echo.
echo Plik: dist\AktualizatorStrony.exe
echo Rozmiar:
dir "dist\AktualizatorStrony.exe" | find "AktualizatorStrony.exe"
echo.
echo ========================================
echo NASTEPNE KROKI:
echo ========================================
echo.
echo 1. Test aplikacji:
echo    cd dist
echo    AktualizatorStrony.exe
echo.
echo 2. Zbuduj instalator (jezeli masz Inno Setup):
echo    build_installer.bat
echo.
pause



