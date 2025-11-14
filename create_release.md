# 📦 Tworzenie Release v5.2.0 w GitHub

## 🎯 Cel
Utworzenie oficjalnego wydania (release) aplikacji w repozytorium GitHub, aby funkcja auto-update działała poprawnie.

---

## 📋 Kroki do wykonania

### Krok 1: Przygotowanie lokalnego repozytorium

```powershell
# Upewnij się, że jesteś w katalogu projektu
cd C:\Users\stare\aplikacja-szpont

# Sprawdź status git
git status

# Dodaj wszystkie zmiany
git add .

# Zatwierdź zmiany
git commit -m "Release v5.2.0 - Poprawka GitHub URL i przygotowanie do auto-update"

# Wypchnij zmiany
git push origin main
```

### Krok 2: Utworzenie tagu wersji (opcjonalnie lokalnie)

```powershell
# Utwórz tag dla wersji 5.2.0
git tag -a v5.2.0 -m "Release v5.2.0 - Auto-update ready"

# Wypchnij tag do GitHub
git push origin v5.2.0
```

### Krok 3: Utworzenie Release w GitHub (GŁÓWNY KROK)

#### Opcja A: Przez interfejs webowy GitHub (ZALECANE dla pierwszego release)

1. **Przejdź do repozytorium:**
   - Otwórz przeglądarkę
   - Idź do: https://github.com/IgorStarega/aplikacja-szpont

2. **Utwórz nowy Release:**
   - Kliknij **"Releases"** (po prawej stronie, w sekcji "About")
   - Kliknij **"Create a new release"** lub **"Draft a new release"**

3. **Wypełnij formularz Release:**
   - **Tag version**: `v5.2.0` (wybierz lub utwórz nowy)
   - **Target**: `main` (wybierz gałąź)
   - **Release title**: `v5.2.0 - Auto-Update Ready`
   - **Description**: (skopiuj poniższy tekst)

```markdown
# 🚀 Aktualizator Strony v5.2.0

## ✨ Co nowego w wersji 5.2.0

### 🔄 Auto-Update System
- ✅ Automatyczne sprawdzanie aktualizacji z GitHub
- ✅ Pobieranie i instalacja nowych wersji
- ✅ Backup przed aktualizacją
- ✅ Rollback w przypadku błędu
- ✅ Powiadomienia o dostępnych aktualizacjach

### 🐛 Poprawki
- ✅ Naprawiono błąd 404 przy sprawdzaniu aktualizacji
- ✅ Poprawiono ścieżkę repozytorium GitHub (IgorStarega/aplikacja-szpont)
- ✅ Dodano obsługę tagów wersji

### 📊 Funkcje istniejące
- ⚡ **Batch Processing** - 3x szybsze przetwarzanie
- 💾 **Smart Caching** - 60% oszczędności czasu
- 📊 **Analytics** - statystyki i raporty (Excel/PDF)
- 📅 **Scheduler** - harmonogram automatycznych aktualizacji
- 💬 **Notifications** - Slack, Discord
- 🌐 **Web Dashboard** - Flask + REST API
- 🐳 **Docker** - gotowy do deployment

---

## 📥 Instalacja

### Opcja 1: Standalone (.exe) - ZALECANE
```bash
# Pobierz i uruchom
uruchom.bat
```

### Opcja 2: Python
```bash
pip install -r requirements.txt
python apk.py
```

### Opcja 3: Docker
```bash
docker-compose up -d
```

---

## 📝 Wymagania
- Python 3.7+
- Windows/Linux/macOS
- SSH access do serwera (opcjonalnie)

---

## 🔗 Dokumentacja
Zobacz [README.md](https://github.com/IgorStarega/aplikacja-szpont/blob/main/README.md) po więcej informacji.

---

**Full Changelog**: https://github.com/IgorStarega/aplikacja-szpont/commits/v5.2.0
```

4. **Dodaj pliki (opcjonalnie):**
   - Jeśli masz skompilowaną wersję `.exe`, możesz ją dodać jako załącznik
   - Możesz dodać plik `requirements.txt`
   - Możesz dodać archiwum ZIP z kodem źródłowym

5. **Publikuj:**
   - ✅ Zaznacz **"Set as the latest release"**
   - Kliknij **"Publish release"**

#### Opcja B: Przez GitHub CLI (szybsze, wymaga zainstalowania gh)

```powershell
# Zainstaluj GitHub CLI (jeśli nie masz)
# Pobierz z: https://cli.github.com/

# Zaloguj się
gh auth login

# Utwórz release
gh release create v5.2.0 `
  --title "v5.2.0 - Auto-Update Ready" `
  --notes "Release v5.2.0 z obsługą automatycznych aktualizacji" `
  --latest
```

---

## ✅ Weryfikacja

Po utworzeniu release sprawdź czy działa:

1. **Sprawdź API endpoint:**
```powershell
curl https://api.github.com/repos/IgorStarega/aplikacja-szpont/releases/latest
```

Powinieneś zobaczyć JSON z informacjami o release v5.2.0

2. **Uruchom aplikację:**
   - Uruchom aplikację
   - Sprawdź czy nie ma błędu 404
   - Sprawdź czy pokazuje się informacja o aktualnej wersji

---

## 🔮 Przyszłe Release'y

Kiedy będziesz tworzył nową wersję (np. 5.3.0):

1. Zaktualizuj `CURRENT_VERSION` w `src/auto_update_manager.py`
2. Zaktualizuj wersję w `README.md` i `config.json`
3. Zatwierdź zmiany w git
4. Utwórz nowy tag i release (powtórz kroki powyżej z nową wersją)

---

## 🆘 Rozwiązywanie problemów

### Release nie pojawia się w API
- Sprawdź czy release jest oznaczony jako "latest"
- Sprawdź czy tag jest poprawny (v5.2.0, nie 5.2.0)
- Poczekaj 1-2 minuty (cache GitHub)

### Błąd 404 nadal występuje
- Sprawdź czy repozytorium jest publiczne
- Sprawdź czy release jest opublikowany (nie draft)
- Sprawdź nazwę repozytorium w kodzie

---

## 📞 Pomoc

Jeśli masz problemy:
1. Sprawdź logi aplikacji w `logs/update.log`
2. Sprawdź czy repozytorium jest publiczne
3. Sprawdź czy tag wersji jest poprawny

---

**Powodzenia! 🚀**

