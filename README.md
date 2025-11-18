# 🚀 Aktualizator Strony v5.3.0

Automatyczna aktualizacja strony **prakt.dziadu.dev** z repozytorium źródłowego.

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Version](https://img.shields.io/badge/version-5.3.0-blue)]()
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)]()
[![New](https://img.shields.io/badge/NEW-v5.3.0%20Features!-orange)]()

---

## ✨ Funkcje

### Core Features (v4.1-5.2)
- ⚡ **Batch Processing** - 3x szybsze przetwarzanie
- 💾 **Smart Caching** - 60% oszczędności czasu
- 🔄 **Auto-Update** - automatyczna aktualizacja aplikacji z GitHub
- 📊 **Analytics** - statystyki i raporty (Excel/PDF)
- 📅 **Scheduler** - harmonogram automatycznych aktualizacji
- 💬 **Notifications** - Slack, Discord
- 🌐 **Web Dashboard** - Flask + REST API
- 🐳 **Docker** - gotowy do deployment
- 🎨 **Ikona Aplikacji** - profesjonalna ikona na pasku zadań i skrócie

### 🆕 Nowe w v5.3.0
- 🎨 **5 Nowych Motywów** - Ocean Blue, Forest Green, Sunset Orange, Purple Dream, Cherry Blossom
- 📊 **Interaktywne Wykresy** - matplotlib i plotly dla wizualizacji danych
- ⌨️ **Skróty Klawiaturowe** - 15+ skrótów (Ctrl+U, Ctrl+S, itp.)
- 🔍 **Zaawansowana Wyszukiwarka** - filtry i regex support
- 💾 **System Snapshots** - backup i rollback z visual diff
- 🌍 **Multi-Repository** - zarządzanie wieloma repozytoriami
- 🛡️ **Auto-Retry** - exponential backoff dla błędów sieci
- 🎯 **Quick Actions Menu** - kontekstowe menu (PPM)
- ⚡ **Lazy Loading** - 70% mniej RAM, 5x szybsze tabele

---

## 🚀 Quick Start

### Opcja 1: Standalone (.exe) - **ZALECANE**

```bash
# Uruchom gotową aplikację (bez instalacji Python!)
uruchom.bat
```

lub

```bash
dist\AktualizatorStrony.exe
```

### Opcja 2: Development

```bash
# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację
python apk.py
```

### Opcja 3: Docker

```bash
docker-compose up -d
```

---

## 📖 Pierwsze użycie

1. **Uruchom aplikację** (patrz Quick Start)
2. **Ustaw ścieżki** w GUI:
   - **Źródło:** Ścieżka do `szkola25-26`
   - **Cel:** Ścieżka do `strona-dziadu-dev`
3. **Kliknij:** "🚀 Aktualizuj Teraz"
4. **Gotowe!** Aplikacja automatycznie zaktualizuje stronę

---

## 🔧 Build

Zbuduj standalone .exe:

```bash
build.bat
```

Wynik: `dist\AktualizatorStrony.exe` (~39 MB)


---

## 🔄 Auto-Update

Aplikacja automatycznie sprawdza aktualizacje przy starcie:
- Łączy się z GitHub Releases
- Pobiera i instaluje nowe wersje automatycznie
- Zachowuje konfigurację użytkownika

Wyłączenie: `config.json` → `"check_updates_on_startup": false`

---

## 📊 Struktura

```
aplikacja-szpont/
├── apk.py                    # Główny punkt wejścia
├── config.json               # Konfiguracja
├── requirements.txt          # Zależności
├── uruchom.bat              # Szybki start
├── build.bat                # Build .exe
├── src/                     # Kod źródłowy
│   ├── gui_modern.py        # GUI (customtkinter)
│   ├── update_manager.py    # Logika aktualizacji
│   ├── database_manager.py  # SQLite
│   └── ...
└── dist/                    # Zbudowana aplikacja
    └── AktualizatorStrony.exe
```

---

## ⚙️ Wymagania

- **Windows:** 7 SP1+ / 8 / 10 / 11
- **Python:** 3.7+ (tylko dla development)
- **Git:** Zainstalowany w systemie
- **Internet:** Do auto-update i Git push

**Dla .exe:** Python NIE jest wymagany!

---

## 📋 Kluczowe funkcje

### Analytics & Reports
- SQLite baza danych historii aktualizacji
- Dashboard ze statystykami
- Eksport do Excel/PDF

### Automatyzacja
- Harmonogram codziennych aktualizacji
- Powiadomienia (Slack/Discord/Email)
- GitHub Webhooks

### Web & API
- Flask Web Dashboard (port 5000)
- REST API endpoints
- Mobile API support

### Production
- Docker & docker-compose
- PyInstaller standalone build
- Auto-update z GitHub Releases

---

## 🛠️ Konfiguracja

Edytuj `config.json`:

```json
{
  "app_version": "5.2",
  "source_path": "C:\\Users\\nazwa\\szkola25-26",
  "target_path": "C:\\Users\\nazwa\\strona-dziadu-dev",
  "theme": "system",
  "check_updates_on_startup": true
}
```

---

## 💡 Docker deployment

```bash
docker-compose up -d
```

Web Dashboard: `http://localhost:5000`

---

## 📄 Licencja

Zobacz `LICENSE.txt`

---

## 🎯 Status

**Wersja:** 5.2  
**Status:** ✅ Production Ready  
**Data:** 2025-11-14  
**Strona:** https://prakt.dziadu.dev

---

**Gotowa do użycia!** 🚀

Więcej informacji: `TODO.md`

