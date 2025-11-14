# 📋 CHANGELOG - Aktualizator Strony

Wszystkie istotne zmiany w projekcie są dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
projekt stosuje [Semantic Versioning](https://semver.org/lang/pl/).

---

## [5.2.0] - 2025-11-14

### ✨ Dodano
- 🎨 **Ikona aplikacji** - profesjonalna ikona na pasku zadań, skrócie i w pliku .exe
- 📦 **Plik ikona.ico** - wielorozmiarowa ikona ICO dla Windows
- 🔄 **Auto-Update Manager** - automatyczna aktualizacja aplikacji z GitHub
- 📱 **Mobile API Manager** - API dla aplikacji mobilnych
- 🐳 **Docker Support** - pełna obsługa Docker i docker-compose
- 📦 **PyInstaller Build** - kompilacja do standalone .exe
- 📝 **ULEPSZENIA.md** - dokument z propozycjami ulepszeń (25 kategorii)
- ⚡ **QUICK_IMPROVEMENTS.md** - gotowe do implementacji poprawki (18 ulepszeń)

### 🔧 Zmieniono
- ✅ Zaktualizowano `requirements.txt` - dodano Pillow
- ✅ Zaktualizowano `build.spec` - dodano ikony do buildu
- ✅ Poprawiono `.github/workflows/tests.yml` - naprawiono błędy CI/CD
- ✅ Zaktualizowano dokumentację w README.md

### 🐛 Naprawiono
- ✅ Obsługa ścieżek PyInstaller dla ikony (sys._MEIPASS)
- ✅ Garbage collection dla PhotoImage (zapisywanie referencji)
- ✅ Błędna składnia w workflow (download/upload artifacts)
- ✅ Deprecated GitHub Actions (create-release → action-gh-release)

---

## [5.1.0] - 2024

### ✨ Dodano
- 🌐 **Web Dashboard** - Flask-based dashboard
- 🔌 **REST API** - pełne API dla integracji
- 🪝 **Webhook Manager** - obsługa webhooków GitHub
- 🔐 **SSH Manager** - zarządzanie kluczami SSH
- 🔑 **Credentials Manager** - bezpieczne przechowywanie credentials

### 🔧 Zmieniono
- Ulepszona architektura modułowa
- Rozszerzona konfiguracja (config.json)

---

## [5.0.0] - 2024

### ✨ Dodano
- 📊 **Database Manager** - SQLite dla historii aktualizacji
- 📈 **Analytics Dashboard** - statystyki i wykresy
- 📄 **Report Generator** - eksport do Excel/PDF
- 📅 **Update Scheduler** - harmonogram aktualizacji
- 💬 **Notification Service** - Slack, Discord, Email
- 🔄 **Incremental Updates** - tylko zmienione pliki
- 📊 **Inteligentne Różnicowanie** - porównywanie HTML

### 🔧 Zmieniono
- Pełna refaktoryzacja architektury
- Nowy system zakładek w GUI
- Rozszerzone logowanie

---

## [4.1.0] - 2024

### ✨ Dodano
- ⚡ **Batch Processing** - ThreadPoolExecutor (+300% szybciej)
- 💾 **Cache Struktury** - MD5 hashing (-60% czasu)
- 🔄 **Asynchroniczne Git** - operacje w tle
- ✨ **CustomTkinter GUI** - nowoczesny interfejs
- 🌙 **Dark/Light Mode** - przełącznik motywów
- ⏱️ **Progress Bar z ETA** - szacowany czas zakończenia
- 🔐 **.env Support** - zmienne środowiskowe

### 🔧 Zmieniono
- Całkowicie nowy GUI (customtkinter)
- Ulepszona wydajność (3x szybciej)

---

## [4.0.0] - 2024

### ✨ Dodano
- Pierwsza wersja z GUI (Tkinter)
- Podstawowa aktualizacja folderów
- Integracja z Git

---

## [3.x] - 2024

### 📝 Notatka
Wersje 3.x były prototypami CLI (Command Line Interface).
Nie są już wspierane.

---

## 🔗 Linki

- [Repository](https://github.com/IgorStarega/aplikacja-szpont)
- [Issues](https://github.com/IgorStarega/aplikacja-szpont/issues)
- [Releases](https://github.com/IgorStarega/aplikacja-szpont/releases)

---

## 📌 Legenda

- ✨ **Dodano** - nowe funkcje
- 🔧 **Zmieniono** - zmiany w istniejących funkcjach
- 🐛 **Naprawiono** - poprawki błędów
- 🗑️ **Usunięto** - usunięte funkcje
- ⚠️ **Deprecated** - funkcje do usunięcia w przyszłości
- 🔒 **Security** - poprawki bezpieczeństwa

---

**Aktualna wersja:** 5.2.0  
**Status:** ✅ PRODUCTION READY  
**Ostatnia aktualizacja:** 2025-11-14

