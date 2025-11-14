@echo off
echo ========================================
echo   Tworzenie Release v5.2.0 w GitHub
echo ========================================
echo.
echo Tag v5.2.0 juz istnieje w repozytorium!
echo Teraz musisz utworzyc Release w GitHub.
echo.
echo KROK 1: Otwieram strone tworzenia Release...
echo.
start https://github.com/IgorStarega/aplikacja-szpont/releases/new?tag=v5.2.0
echo.
echo KROK 2: Wypelnij formularz na stronie GitHub:
echo.
echo   Tag: v5.2.0 (powinien byc juz wybrany)
echo   Release title: v5.2.0 - Auto-Update Ready
echo   Description: (skopiuj ponizej)
echo.
echo ========================================
echo OPIS DO SKOPIOWANIA:
echo ========================================
type RELEASE_NOTES_v5.2.0.md
echo.
echo ========================================
echo.
echo KROK 3: Po wypelnieniu:
echo   [x] Zaznacz "Set as the latest release"
echo   [ ] Kliknij "Publish release"
echo.
echo KROK 4: Poczekaj 1-2 minuty i uruchom aplikacje ponownie
echo.
pause

