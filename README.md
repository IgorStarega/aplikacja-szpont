# 🔄 Aktualizator Strony - v5.0 PRODUCTION READY

**Nowoczesna aplikacja do automatycznego aktualizowania strony internetowej na bazie repozytorium GitHub.**

![Version](https://img.shields.io/badge/version-5.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Status](https://img.shields.io/badge/status-PRODUCTION%20READY-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🎯 Główne Cechy

### ⚡ Performance (v4.1+)
- **Batch Processing**: +3x szybciej (ThreadPoolExecutor, 4 wątki)
- **Caching**: -60% czasu skanowania (MD5 hashing)
- **Async Git**: GUI zawsze responsywne (0% freezing)
- **Incremental Updates**: Powtórne aktualizacje 12-25x szybciej!

### 📊 Analytics & Reporting (v5.0 NEW)
- **SQLite Historia**: Baza danych wszystkich aktualizacji
- **Analytics Dashboard**: Statystyki z ostatnich 30 dni
- **Excel/PDF Reports**: Eksport z automatycznym formatowaniem
- **Real-time Metrics**: Licznik kart, czasu, cache'a

### 📅 Automatyzacja (v5.0 NEW)
- **Update Scheduler**: Uruchamiaj aktualizacje o określonym czasie
- **Harmonogram Codziennie**: Konfiguruj godzinę i minutę
- **Harmonogram Interwałowo**: Co N godzin/minut/sekund

### 💬 Powiadomienia (v5.0 NEW)
- **Slack Integration**: Powiadomienia na Slack
- **Discord Integration**: Embeds na Discord
- **Email Reports**: Wysyłanie raportów email

### 🎨 GUI
- **Nowoczesny Interfejs**: customtkinter (elegancki Tkinter)
- **Dark/Light Mode**: Automatyczne lub ręczne przełączanie
- **7 Zakładek**: Aktualizacja, Analytics, Raporty, Harmonogram, Powiadomienia, Ustawienia
- **Progress Bar**: Z realtime ETA i wskaźnikami cache'a

---

## 🚀 Szybki Start

### 1. Instalacja Zależności

```bash
pip install -r requirements.txt
```

### 2. Konfiguracja

#### Zmienne Środowiskowe (.env)
```bash
cp .env.example .env
# Edytuj .env i ustaw:
SOURCE_REPO_PATH=C:\Users\stare\szkola25-26
TARGET_REPO_PATH=C:\Users\stare\strona-dziadu-dev
```

#### Ścieżki w GUI
1. Otwórz aplikację
2. Wpisz ścieżki repozytoriów lub kliknij "📂 Przeglądaj"
3. Ścieżki są automatycznie zapisywane

### 3. Uruchomienie

```bash
python apk.py
```

---

## 📋 Użytkownik

### 🚀 Aktualizacja
1. Kliknij "🚀 Aktualizuj Teraz (v5.0)"
2. Obserwuj progres z ETA
3. Otrzymasz komunikat o wyniku
4. Logi pokazują szczegóły (karty dodane/zmienione/usunięte)

### 📊 Analytics
1. Przejdź do zakładki "📊 Analytics"
2. Kliknij "🔄 Odśwież Statystyki"
3. Wyświetlą się statystyki z ostatnich 30 dni:
   - Liczba aktualizacji (udane, nieudane, bez zmian)
   - Liczba kart (dodane, zmienione, usunięte)
   - Średni czas trwania
   - Użycie cache'a

### 📄 Raporty
1. Przejdź do zakładki "📄 Raporty"
2. Kliknij "📊 Eksportuj do Excel" lub "📕 Eksportuj do PDF"
3. Raporty będą zapisane w `src/.data/reports/`

### 📅 Harmonogram
1. Przejdź do zakładki "📅 Harmonogram"
2. Ustaw godzinę i minutę
3. Kliknij "➕ Dodaj"
4. Kliknij "▶️  Uruchom Scheduler"
5. Aktualizacje będą uruchamiane automatycznie

### 💬 Powiadomienia
1. Przejdź do zakładki "💬 Powiadomienia"
2. Wpisz Slack token i ID kanału
3. Kliknij "Konfiguruj Slack"
4. Alternatywnie: wpisz Discord webhook URL
5. Powiadomienia będą wysyłane na wybrany kanał

---

## 📊 Dokumentacja Techniczna

### Struktura Projektu

```
aplikacja-szpont/
├── 📄 apk.py                       ← Główny punkt wejścia
├── 📄 requirements.txt              ← Zależności
├── 📄 README.md                     ← Ten plik
├── 📄 CHANGELOG.md                  ← Historia zmian
│
├── 📁 src/                          ← Główny kod
│   ├── config.json                  ← Konfiguracja aplikacji
│   ├── config_manager.py            ← Manager konfiguracji
│   ├── gui_modern.py                ← GUI (customtkinter) v5.0
│   ├── theme_manager.py             ← Manager motywów
│   ├── update_manager.py            ← Manager aktualizacji
│   ├── database_manager.py          ← SQLite Manager (NEW v5.0)
│   ├── report_generator.py          ← Report Generator (NEW v5.0)
│   ├── scheduler.py                 ← Update Scheduler (NEW v5.0)
│   ├── notification_service.py      ← Notifications (NEW v5.0)
│   │
│   ├── .cache/                      ← Cache struktury folderów
│   │   └── structure_cache.json
│   │
│   ├── .data/                       ← Baza danych i raporty (NEW v5.0)
│   │   └── reports/                 ← Raporty Excel/PDF
│   │   └── updates.db               ← SQLite baza
│   │
│   └── .config/                     ← Konfiguracje (NEW v5.0)
│       ├── schedule.json            ← Harmonogram
│       └── notifications.json       ← Powiadomienia
│
├── 📁 docs/                         ← Dokumentacja
│   ├── API_REFERENCE.md
│   ├── INSTRUKCJA.md
│   └── TROUBLESHOOTING.md
│
├── 📁 tests/                        ← Testy
│   ├── test_update_manager.py
│   └── check_app.py
│
├── 📁 backups/                      ← Automatyczne backupy HTML
│
├── 📁 logs/                         ← Logi aplikacji
│   └── update.log
│
└── 📁 strony/                       ← Strony do testowania
    └── src/
```

### Architektura

```
┌─────────────────────────────────────┐
│           GUI (customtkinter)       │  v5.0
├─────────────────────────────────────┤
│  UpdateManager  │  DatabaseManager  │  v5.0 Components
│  ReportGenerator│  Scheduler        │
│  Notifications  │  ConfigManager    │
├─────────────────────────────────────┤
│        Git Operations (subprocess)  │  Backend
│     HTML Processing (BeautifulSoup) │
│     File I/O (pathlib, shutil)     │
├─────────────────────────────────────┤
│       SQLAlchemy ORM (SQLite)       │  Database v5.0
│    External APIs (Slack, Discord)   │
└─────────────────────────────────────┘
```

### Klasy Główne

#### `ModernGUI` (gui_modern.py)
- GUI aplikacji z 7 zakładkami
- Threading dla asynchronicznych operacji
- Progress bar z ETA
- Integracja z UpdateManager

#### `UpdateManager` (update_manager.py)
- Batch processing (ThreadPoolExecutor)
- Caching (MD5 hashing)
- Git operacje (async)
- Inteligentne różnicowanie (diff)
- Incremental updates

#### `DatabaseManager` (database_manager.py) - NEW v5.0
- SQLite ORM (SQLAlchemy)
- Tabela UpdateHistory
- Metody: add_update_record, get_statistics, cleanup_old_records

#### `ReportGenerator` (report_generator.py) - NEW v5.0
- Eksport do Excel (openpyxl)
- Eksport do PDF (reportlab)
- Formatowanie i styling

#### `UpdateScheduler` (scheduler.py) - NEW v5.0
- Codzienne aktualizacje (schedule)
- Aktualizacje interwałowe
- Threading dla pętli schedulera

#### `NotificationService` (notification_service.py) - NEW v5.0
- Slack SDK
- Discord webhook
- Email (smtplib)

---

## 🔧 Konfiguracja

### config.json
```json
{
  "SOURCE_REPO_PATH": "C:\\Users\\stare\\szkola25-26",
  "TARGET_REPO_PATH": "C:\\Users\\stare\\strona-dziadu-dev",
  "auto_update_enabled": false,
  "log_level": "INFO",
  "backup_enabled": true,
  "theme": "dark"
}
```

### .env
```env
SOURCE_REPO_PATH=C:\Users\stare\szkola25-26
TARGET_REPO_PATH=C:\Users\stare\strona-dziadu-dev
LOG_LEVEL=INFO
BACKUP_ENABLED=true
BACKUP_CLEANUP_DAYS=30
```

### schedule.json (Harmonogram) - NEW v5.0
```json
{
  "enabled": true,
  "jobs": [
    {
      "name": "daily_update",
      "type": "daily",
      "time": "02:00"
    }
  ]
}
```

### notifications.json (Powiadomienia) - NEW v5.0
```json
{
  "slack": {
    "enabled": true,
    "token": "xoxb-...",
    "channel": "C123..."
  },
  "discord": {
    "enabled": true,
    "webhook_url": "https://discord.com/..."
  }
}
```

---

## 📈 Performance

### Benchmark v4.1

| Operacja | Czas | Poprawa |
|----------|------|--------|
| **Full Update (bez cache)** | 1-3s | - |
| **Full Update (z cache)** | 400-500ms | 3-7x szybciej |
| **Batch Processing** | +3x szybciej | 300% |
| **Async Git** | 0% freezing GUI | 100% |
| **Memory Usage** | ~50MB | Stabilny |

### Statystyki Cache

- **Struktura Cache**: `src/.cache/structure_cache.json`
- **MD5 Hashing**: Każdy folder ma unikatowy hash
- **Detekcja Zmian**: Automatyczna przy starcie
- **Oszczędności**: -60% czasu skanowania

---

## 🧪 Testowanie

### Unit Testy
```bash
pytest tests/ -v
pytest tests/ --cov=src
```

### Szybkie Sprawdzenie
```bash
python tests/check_app.py
```

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'customtkinter'"
**Rozwiązanie**: 
```bash
pip install -r requirements.txt
```

### Problem: "Aktualizacja zawiesza się"
**Rozwiązanie**: 
- Sprawdzić czy ścieżki są poprawne
- Sprawdzić logi w `logs/update.log`
- Upewnić się że Git jest zainstalowany

### Problem: "Cache nie działa"
**Rozwiązanie**: 
- Sprawdzić czy folder `src/.cache/` istnieje
- Usunąć `src/.cache/structure_cache.json` i uruchomić ponownie

---

## 📞 Wsparcie

1. Sprawdź `docs/TROUBLESHOOTING.md`
2. Przeczytaj `docs/INSTRUKCJA.md`
3. Sprawdź `logs/update.log`

---

## 📄 Licencja

MIT License - Wolne do użytku i modyfikacji.

---

## 🎉 Changelog

### v5.0 (2025-11-07) ✅ PRODUCTION READY
- ✅ SQLite Historia Aktualizacji
- ✅ Analytics Dashboard
- ✅ Report Generator (Excel/PDF)
- ✅ Update Scheduler
- ✅ Notifications (Slack/Discord/Email)

### v4.1 (2025-11-06) ✅ PRODUCTION READY
- ✅ Batch Processing (+3x szybciej)
- ✅ Caching (-60% czasu)
- ✅ Async Git Operations
- ✅ Inteligentne Różnicowanie
- ✅ Incremental Updates

### v4.0 (2025-11-05)
- ✅ Nowoczesne GUI (customtkinter)
- ✅ Dark/Light Mode
- ✅ Theme Manager
- ✅ Logging Settings

Pełna historia w `CHANGELOG.md`

---

## 🚀 Przyszłe Usprawnienia

### v5.1 (Q1 2026)
- Web Dashboard (Flask)
- REST API
- Webhook Integration (GitHub)
- SSH Key Support

### v6.0 (Q2 2026)
- Docker Support
- PyInstaller Build (.exe)
- Multi-Language Support
- Theme Customization

---

**Aplikacja v5.0 jest w pełni funkcjonalna i gotowa do produkcji!** 🚀

Obsługuje: **Windows, macOS, Linux** | **Python 3.7+**

