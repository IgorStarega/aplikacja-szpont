# 🚀 Szybki przewodnik - Tworzenie Release v5.2.0

## ✅ Co zostało zrobione automatycznie:
1. ✅ Poprawiono błąd 404 w URL GitHub (IgorStarega/aplikacja-szpont)
2. ✅ Zaktualizowano `src/auto_update_manager.py`
3. ✅ Zaktualizowano `src/gui_modern.py`
4. ✅ Utworzono dokumentację release
5. ✅ Utworzono skrypty pomocnicze
6. ✅ Zaktualizowano .gitignore

## 📝 Co musisz zrobić teraz:

### KROK 1: Zatwierdź zmiany w Git
```powershell
cd C:\Users\stare\aplikacja-szpont

# Dodaj wszystkie pliki
git add .

# Zatwierdź zmiany
git commit -m "Release v5.2.0 - Auto-Update Ready, poprawka GitHub URL"

# Wypchnij do GitHub
git push origin main
```

### KROK 2: Utwórz tag wersji
```powershell
# Utwórz tag
git tag -a v5.2.0 -m "Release v5.2.0 - Auto-Update Ready"

# Wypchnij tag do GitHub
git push origin v5.2.0
```

### KROK 3: Utwórz Release w GitHub

#### Opcja A: Przez przeglądarkę (ZALECANE)
1. Otwórz: https://github.com/IgorStarega/aplikacja-szpont/releases/new
2. Wypełnij formularz:
   - **Tag**: wybierz `v5.2.0`
   - **Title**: `v5.2.0 - Auto-Update Ready`
   - **Description**: skopiuj zawartość z `RELEASE_NOTES_v5.2.0.md`
3. Zaznacz: "Set as the latest release"
4. Kliknij: "Publish release"

#### Opcja B: Przez GitHub CLI (jeśli zainstalowane)
```powershell
gh release create v5.2.0 --title "v5.2.0 - Auto-Update Ready" --notes-file RELEASE_NOTES_v5.2.0.md --latest
```

### KROK 4: Weryfikacja
```powershell
# Sprawdź czy release jest widoczny w API
curl https://api.github.com/repos/IgorStarega/aplikacja-szpont/releases/latest
```

Lub otwórz w przeglądarce:
https://github.com/IgorStarega/aplikacja-szpont/releases

### KROK 5: Test
1. Uruchom aplikację: `python apk.py`
2. Sprawdź czy nie ma błędu 404
3. Sprawdź czy aplikacja wykrywa wersję 5.2.0

---

## 🆘 Problemy?

### "Tag już istnieje"
```powershell
# Usuń lokalny tag
git tag -d v5.2.0

# Usuń zdalny tag
git push origin --delete v5.2.0

# Utwórz ponownie (KROK 2)
```

### "Release nie pojawia się w API"
- Poczekaj 1-2 minuty (cache GitHub)
- Sprawdź czy release jest "published" (nie "draft")
- Sprawdź czy repozytorium jest publiczne

### "Błąd 404 nadal występuje"
- Sprawdź czy utworzyłeś release (KROK 3)
- Sprawdź czy tag to dokładnie `v5.2.0`
- Zrestartuj aplikację

---

## ✨ Po wykonaniu tych kroków:
- ✅ Auto-update będzie działać
- ✅ Aplikacja będzie sprawdzać aktualizacje z GitHub
- ✅ Błąd 404 zniknie

**Powodzenia! 🚀**

