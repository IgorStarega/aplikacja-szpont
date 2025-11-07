# 📖 INSTRUKCJA OBSŁUGI - Aktualizator Strony v2.4

## 🚀 Szybki Start

### 1. Instalacja

```bash
cd "C:\Users\stare\Aplikacja do aktualizacji strony"
pip install -r requirements.txt
```

### 2. Uruchomienie

```bash
python apk.py
```

## 📝 Przewodnik po Interfejsie

### 💻 Karta "Aktualizacja"

**Ścieżki repozytoriów:**
- **Źródło (szkola25-26):** Ścieżka do repozytorium ze źródłowymi plikami
- **Cel (strona-dziadu-dev):** Ścieżka do repozytorium strony do aktualizacji

**Przyciski:**
- 🔄 **Aktualizuj teraz** - Uruchamia jednorazową aktualizację
- 🗑️ **Wyczyść logi** - Czyści okno logów

**Logi aktualizacji:**
- Pokazuje co się dzieje krok po kroku
- [HH:MM:SS] Timestamp dla każdej operacji

**Podsumowanie:**
- Dodane, Zmodyfikowane, Usunięte karty

---

### 📋 Karta "Historia"

- Wyświetla ostatnie 20 aktualizacji
- Kolumny: Data i czas, Dodane, Zmodyfikowane, Usunięte, Foldery
- 🔄 **Odśwież** - Odświeża listę

---

### ⚙️ Karta "Ustawienia"

**Automatyczne aktualizacje:**
- ☑️ **Włącz automatyczne aktualizacje** - Checkbox
- **Interwał:** Liczba (domyślnie 60)
- **Jednostka:** Minuty / Godziny

**Przyciski:**
- 💾 **Zapisz ustawienia** - Zapisuje konfigurację

---

## 🔄 Proces Aktualizacji

### Co się dzieje w trakcie aktualizacji:

1. **🔍 Walidowanie repozytoriów** - Sprawdza czy foldery istnieją
2. **📤 Aktualizowanie repozytoriów** - Pobiera najnowsze zmiany (`git pull`)
3. **📝 Aktualizowanie plików HTML** - Generuje/aktualizuje karty HTML
4. **📤 Commitowanie i push** - Wysyła zmiany do Git

### Foldery które się synchronizują:
- `desktopy/` → `desktopy.html`
- `TSiAI/` → `TSiAI.html`
- `WiAI/` → `WiAI.html`
- `informatyka/` → `informatyka.html`

---

## 🎯 Najczęstsze Operacje

### Jednorazowa aktualizacja:
1. Wpisz/wybierz ścieżki
2. Kliknij "🔄 Aktualizuj teraz"
3. Czekaj na wynik

### Włączenie automatycznych aktualizacji:
1. Przejdź do "⚙️ Ustawienia"
2. Zaznacz "Włącz automatyczne aktualizacje"
3. Ustaw interwał
4. Kliknij "💾 Zapisz ustawienia"

### Przeglądanie historii:
1. Kliknij kartę "📋 Historia"
2. Przejrzyj ostatnie aktualizacje
3. Kliknij "🔄 Odśwież" aby zobaczyć najnowsze

---

## 📊 Zrozumienie Podsumowania

| Symbol | Znaczenie |
|--------|-----------|
| ➕ Dodane | Nowe karty zostały dodane do strony |
| ✏️ Zmodyfikowane | Istniejące strony HTML zostały zmienione |
| 🗑️ Usunięte | Karty zostały usunięte (bo zadania zniknęły) |
| 📁 Foldery | Które foldery zostały zaktualizowane |

---

## 🔒 Automatyczne Backupy

**Gdzie są?** Folder `backups/`

**Format nazwy:** `[strona]_backup_YYYYMMDD_HHMMSS.html`

Np: `desktopy_backup_20250106_120000.html`

**Automatyczne czyszczenie:** Backupy starsze niż 30 dni są usuwane

---

## 📁 Struktura Folderów

```
Źródło (szkoła25-26):
├── desktopy/
│   ├── sekcja1/
│   │   ├── zadanie1/
│   │   │   └── index.html
│   │   └── zadanie2.html
│   └── sekcja2/

Cel (strona-dziadu-dev):
├── desktopy.html        ← Automatycznie generowany!
├── TSiAI.html
├── WiAI.html
└── informatyka.html
```

---

## 🎓 Formaty Zadań (Obsługiwane)

**Pojedyncze pliki:**
```
sekcja/
├── zadanie1.html
├── zadanie2.html
└── zadanie3.html
```

**Foldery:**
```
sekcja/
├── zadanie1/
│   └── index.html
├── zadanie2/
│   └── index.html
```

**Mix:**
```
sekcja/
├── zadanie1.html         ← Plik
├── zadanie2/             ← Folder
│   └── index.html
└── Podszona/
    └── zadanie3/
        └── index.html
```

---

## 💾 Pliki Konfiguracji

**config.json:**
- `source_path` - Ścieżka do szkoła25-26
- `target_path` - Ścieżka do strona-dziadu-dev
- `auto_update_enabled` - Czy włączone auto-aktualizacje
- `auto_update_interval` - Interwał
- `update_history` - Historia ostatnich 50 aktualizacji

---

## ⌨️ Klawisze i Skróty

| Akcja | Jak |
|-------|-----|
| Uruchom aktualizację | Kliknij guzik lub Enter |
| Wymuś odświeżenie historii | Kliknij "Odśwież" |
| Zamknij aplikację | Alt+F4 lub "X" |

---

## 📞 Potrzebujesz Pomocy?

Przejrzyj plik: `docs/TROUBLESHOOTING.md`

