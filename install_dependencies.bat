@echo off
echo Instalowanie zależności dla aplikacji...
echo.

REM Pobranie aktualnej ścieżki Python
for /f "delims=" %%i in ('py -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%i

echo Znaleziono Python: %PYTHON_PATH%
echo.

REM Instalacja zależności
echo Instalowanie pakietów...
%PYTHON_PATH% -m pip install --upgrade pip
%PYTHON_PATH% -m pip install customtkinter beautifulsoup4 python-dotenv pytest pytest-cov

echo.
echo Instalacja ukończona!
echo.
pause

