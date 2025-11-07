# 🆘 TROUBLESHOOTING - Rozwiązywanie Problemów

## ❓ FAQ - Częste Pytania

### P: Aplikacja się nie uruchamia
**A:** Sprawdź czy masz zainstalowany Python 3.7+
```bash
python --version
```
Jeśli nie, zainstaluj: https://www.python.org/downloads/

---

### P: Błąd "ModuleNotFoundError"
**A:** Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

---

### P: Nie widzi repozytoriów
**A:** Upewnij się że:
1. Ścieżka jest poprawna (kopiuj z Windows Explorer)
2. Folder zawiera `.git` (repozytorium Git)
3. Masz dostęp do folderu

---

### P: Git nie aktualizuje się
**A:** Sprawdzenia:
1. Czy masz Git zainstalowany? `git --version`
2. Czy masz internetowe połączenie?
3. Czy masz uprawnienia do repozytorium?

---

## 🔴 Typowe Błędy

### "Brak folderu .git w..."
**Przyczyna:** Ścieżka nie jest repozytorium Git

**Rozwiązanie:**
```bash
# Przejdź do folderu
cd "C:\Users\stare\szkoła25-26"
# Sprawdź czy .git istnieje
dir /a | find ".git"
```

---

### "Błąd kodowania pliku HTML"
**Przyczyna:** Plik HTML ma złą kodowanie (np. latin1 zamiast UTF-8)

**Rozwiązanie:**
1. Otwórz plik w Notepad++
2. Kliknij Encoding → Encode in UTF-8
3. Zapisz

---

### "Nie znaleziono content-wrapper"
**Przyczyna:** Struktura HTML się zmieniła lub plik jest złamany

**Rozwiązanie:**
1. Sprawdź backup: `backups/` folder
2. Przywróć z backupu
3. Sprawdź strukturę HTML w pliku `desktopy.html`

---

### "Brak zmian do commitowania"
**Przyczyna:** Nie ma zmian między wersjami

**To jest normalne!** Jeśli nic się nie zmieniło, git nie commituje.

---

### "Push failed"
**Przyczyna:** Problem z dostępem do repozytoria lub internetem

**Rozwiązanie:**
```bash
# Sprawdź czy masz dostęp
git remote -v
# Spróbuj ręcznie
git -C "C:\ścieżka\do\repo" push
```

---

## 🐛 Debugowanie

### Włącz Detailed Log:
1. Uruchom aplikację
2. Karta "📥 Aktualizacja"
3. Sprawdź pole "Logi aktualizacji" - tam są wszystkie detale

### Sprawdź Plik Loga:
```bash
# Logi zapisywane są tutaj
type logs\update.log

# Ostatnie linie
type logs\update.log | tail -50
```

### Testuj Ręcznie:
```bash
# Test Git
git -C "C:\Users\stare\szkoła25-26" status

# Test Python
python -c "from src.update_manager import UpdateManager; print('OK')"
```

---

## 🔧 Zaawansowane Naprawy

### Zresetuj Konfigurację:
```bash
# Usuń config.json
del config.json

# Aplikacja utworzy nowy przy starcie
python apk.py
```

### Wyczyść Backupy:
```bash
# Usuń wszystkie backupy
rmdir /s backups
```

### Wyczyść Logi:
```bash
# Usuń wszystkie logi
del logs\*.log
```

---

## 📞 Kiedy Szukać Pomocy

Jeśli problem nadal istnieje:

1. **Sprawdź Logi:**
   - Plik: `logs/update.log`
   - Szukaj `❌` lub `ERROR`

2. **Sprawdź Strukturę:**
   - Czy `.git` foldery istnieją?
   - Czy ścieżki są prawidłowe?

3. **Test Ręczny:**
   - Spróbuj `git pull` ręcznie
   - Spróbuj otworzyć HTML w przeglądarce

4. **Resetuj:**
   - Usuń `config.json`
   - Usuń `backups/`
   - Zainstaluj zależności na nowo

---

## ✅ Weryfikacja Poprawności

### Aplikacja Działa Prawidłowo Jeśli:
- ✅ Uruchamia się bez błędów
- ✅ Zapamiętuje ścieżki w config.json
- ✅ Pokazuje logi aktualizacji
- ✅ Tworzy backupy w `backups/`
- ✅ Zapisuje logi w `logs/update.log`
- ✅ Commituje zmiany do Git

### Test Pełny:
```bash
# 1. Uruchom aplikację
python apk.py

# 2. Ustaw ścieżki
# 3. Kliknij "Aktualizuj teraz"
# 4. Czekaj na "✅ Aktualizacja zakończona!"

# 5. Sprawdzenie backupu
dir backups
# Powinno pokazać: [strona]_backup_YYYYMMDD_HHMMSS.html

# 6. Sprawdzenie logów
type logs\update.log
# Powinno zawierać: "🔄 Rozpoczynanie..." i "✅ Aktualizacja zakończona!"
```

---

## 📊 Informacje Systemowe

**Wymogi:**
- Python 3.7+
- Git 2.0+
- Windows 10+ (lub Linux/Mac)
- 100MB wolnego miejsca

**Zalecane:**
- Python 3.10+
- 500MB wolnego miejsca
- Szybkie połączenie internetowe

---

**Ostatnia aktualizacja:** 2025-01-06  
**Wersja aplikacji:** 2.4

