# 📚 Dokumentacja Nowych Modułów v5.3.0

## Przegląd

Wersja 5.3.0 wprowadza 4 nowe moduły rozszerzające funkcjonalność aplikacji:

1. **snapshot_manager.py** - System snapshots i rollback
2. **keyboard_shortcuts.py** - Skróty klawiaturowe
3. **multi_repository_manager.py** - Zarządzanie wieloma repozytoriami
4. **visualization_manager.py** - Wykresy i wizualizacje

---

## 1. 💾 Snapshot Manager

### Opis
Moduł do zarządzania snapshotami (kopiami zapasowymi) folderów. Umożliwia tworzenie, porównywanie i przywracanie snapshots.

### Lokalizacja
`src/snapshot_manager.py`

### Główne klasy
- `SnapshotManager` - główna klasa zarządzająca

### Przykład użycia

```python
from snapshot_manager import SnapshotManager
from pathlib import Path

# Inicjalizacja
sm = SnapshotManager(base_path=Path("./snapshots"))

# Stwórz snapshot
snapshot = sm.create_snapshot(
    source_path=Path("./my_project"),
    name="pre_update_backup",
    description="Backup przed dużą aktualizacją",
    tags=["important", "manual"],
    auto=False
)

print(f"✅ Snapshot utworzony: {snapshot['name']}")
print(f"📊 Rozmiar: {snapshot['size_mb']:.2f} MB")

# Lista snapshots
snapshots = sm.list_snapshots(manual_only=True)
for snap in snapshots:
    print(f"- {snap['name']} | {snap['timestamp']} | {snap['description']}")

# Porównaj dwa snapshoty
if len(snapshots) >= 2:
    diff = sm.compare_snapshots(snapshots[0]['name'], snapshots[1]['name'])
    print(f"Dodane pliki: {len(diff['added'])}")
    print(f"Usunięte pliki: {len(diff['removed'])}")
    print(f"Zmodyfikowane: {len(diff['modified'])}")

# Visual diff dla konkretnego pliku
if diff['modified']:
    file_to_compare = diff['modified'][0]
    diff_output = sm.visual_diff(
        snapshots[0]['name'], 
        snapshots[1]['name'], 
        file_to_compare
    )
    print(diff_output)

# Przywróć snapshot
sm.restore_snapshot(
    snapshot_name="pre_update_backup",
    target_path=Path("./my_project")
)

# Cleanup starych snapshots
sm.cleanup_old_snapshots(keep_last=10, keep_manual=True)
```

### Metody

| Metoda | Opis |
|--------|------|
| `create_snapshot()` | Utwórz nowy snapshot |
| `list_snapshots()` | Wyświetl listę snapshots |
| `restore_snapshot()` | Przywróć snapshot |
| `delete_snapshot()` | Usuń snapshot |
| `compare_snapshots()` | Porównaj dwa snapshoty |
| `visual_diff()` | Visual diff dla pliku |
| `cleanup_old_snapshots()` | Wyczyść stare snapshoty |
| `get_snapshot_info()` | Pobierz info o snapshot |

---

## 2. ⌨️ Keyboard Shortcuts Manager

### Opis
Moduł do zarządzania skrótami klawiaturowymi i kontekstowymi menu (prawy przycisk myszy).

### Lokalizacja
`src/keyboard_shortcuts.py`

### Główne klasy
- `KeyboardShortcutsManager` - zarządzanie skrótami
- `QuickActionsMenu` - kontekstowe menu (PPM)

### Przykład użycia

```python
from keyboard_shortcuts import KeyboardShortcutsManager, QuickActionsMenu
import tkinter as tk

# Stwórz okno
root = tk.Tk()

# Inicjalizacja managera
shortcuts_manager = KeyboardShortcutsManager(root)

# Zdefiniuj callbacki
def start_update():
    print("🚀 Rozpoczynam aktualizację...")

def open_settings():
    print("⚙️ Otwieram ustawienia...")

def show_history():
    print("📜 Pokazuję historię...")

# Zarejestruj callbacki
shortcuts_manager.register_callback('start_update', start_update)
shortcuts_manager.register_callback('open_settings', open_settings)
shortcuts_manager.register_callback('show_history', show_history)

# Binduj wszystkie skróty
shortcuts_manager.bind_all_shortcuts()

# Wyświetl pomoc
print(shortcuts_manager.get_shortcuts_help_text())

# Quick Actions Menu dla widgetu
text_widget = tk.Text(root)
text_widget.pack()

quick_menu = QuickActionsMenu(root)
quick_menu.create_menu(text_widget, {
    "Kopiuj": lambda: print("Copy"),
    "Wklej": lambda: print("Paste"),
    "separator": None,
    "Wyczyść": lambda: text_widget.delete("1.0", "end")
})

root.mainloop()
```

### Domyślne skróty

| Skrót | Akcja |
|-------|-------|
| `Ctrl+U` | Rozpocznij aktualizację |
| `Ctrl+S` | Otwórz ustawienia |
| `Ctrl+H` | Pokaż historię |
| `Ctrl+R` / `F5` | Odśwież widok |
| `Ctrl+F` | Wyszukaj |
| `Ctrl+N` | Nowy snapshot |
| `Ctrl+B` | Zarządzaj backupami |
| `Ctrl+T` | Zmień motyw |
| `Ctrl+Q` | Zamknij aplikację |
| `F1` | Pomoc |
| `Ctrl+1-5` | Nawigacja zakładek |

### Metody

| Metoda | Opis |
|--------|------|
| `register_callback()` | Zarejestruj callback |
| `bind_all_shortcuts()` | Binduj wszystkie skróty |
| `unbind_all()` | Usuń wszystkie bindingi |
| `add_shortcut()` | Dodaj nowy skrót |
| `remove_shortcut()` | Usuń skrót |
| `reset_to_defaults()` | Reset do domyślnych |
| `get_shortcuts_help_text()` | Tekst pomocy |

---

## 3. 🌍 Multi Repository Manager

### Opis
Moduł do zarządzania wieloma repozytoriami Git jednocześnie, z obsługą zależności i profili.

### Lokalizacja
`src/multi_repository_manager.py`

### Główne klasy
- `MultiRepositoryManager` - zarządzanie repozytoriami
- `Repository` - dataclass reprezentujący repo
- `RepoProfile` - enum z profilami (dev/staging/prod)

### Przykład użycia

```python
from multi_repository_manager import MultiRepositoryManager, RepoProfile
from pathlib import Path

# Inicjalizacja
mrm = MultiRepositoryManager()

# Dodaj repozytoria
mrm.add_repository(
    name="backend-api",
    local_path="./repos/backend",
    remote_url="https://github.com/user/backend-api.git",
    branch="main",
    profile=RepoProfile.PRODUCTION.value,
    priority=1,
    description="Backend API"
)

mrm.add_repository(
    name="frontend-app",
    local_path="./repos/frontend",
    remote_url="https://github.com/user/frontend-app.git",
    branch="main",
    profile=RepoProfile.PRODUCTION.value,
    priority=2,
    depends_on=["backend-api"],  # Zależy od backend
    description="Frontend aplikacji"
)

# Lista repozytoriów
repos = mrm.list_repositories(profile="production", enabled_only=True)
for repo in repos:
    print(f"📁 {repo.name} - {repo.description}")

# Kolejność aktualizacji (z uwzględnieniem zależności)
update_order = mrm.get_update_order()
print("\n🔄 Kolejność aktualizacji:")
for i, repo in enumerate(update_order, 1):
    print(f"  {i}. {repo.name}")

# Statystyki
stats = mrm.get_statistics()
print(f"\n📊 Statystyki:")
print(f"  Total: {stats['total']}")
print(f"  Enabled: {stats['enabled']}")
print(f"  Production: {stats['by_profile']['production']}")

# Walidacja zależności
errors = mrm.validate_dependencies()
if not errors:
    print("✅ Wszystkie zależności poprawne")

# Export/Import konfiguracji
mrm.export_config(Path("repos_backup.json"))
# mrm.import_config(Path("repos_backup.json"), merge=True)

# Bulk operations
mrm.bulk_update_status(status=True, profile="production")

# Oznacz jako zaktualizowany
mrm.mark_updated("backend-api")
```

### Metody

| Metoda | Opis |
|--------|------|
| `add_repository()` | Dodaj repozytorium |
| `remove_repository()` | Usuń repozytorium |
| `update_repository()` | Zaktualizuj dane repo |
| `get_repository()` | Pobierz repo po nazwie |
| `list_repositories()` | Lista repozytoriów |
| `get_update_order()` | Kolejność aktualizacji |
| `bulk_update_status()` | Włącz/wyłącz wiele |
| `get_statistics()` | Statystyki |
| `validate_dependencies()` | Sprawdź zależności |
| `export_config()` | Eksportuj konfigurację |
| `import_config()` | Importuj konfigurację |

---

## 4. 📊 Visualization Manager

### Opis
Moduł do tworzenia interaktywnych wykresów i wizualizacji za pomocą matplotlib i plotly.

### Lokalizacja
`src/visualization_manager.py`

### Główne klasy
- `VisualizationManager` - zarządzanie wizualizacjami

### Przykład użycia

```python
from visualization_manager import VisualizationManager
from pathlib import Path

# Inicjalizacja
vm = VisualizationManager()

# 1. Wykres trendów (matplotlib)
chart_path = vm.generate_trend_chart(
    days=30, 
    use_plotly=False,
    output_path=Path("./charts/trend.png")
)
print(f"📊 Wykres zapisany: {chart_path}")

# 2. Wykres trendów (plotly - interaktywny)
interactive_chart = vm.generate_trend_chart(
    days=30,
    use_plotly=True
)
print(f"🌐 Interaktywny wykres: {interactive_chart}")

# 3. Heatmapa aktywności
heatmap_path = vm.generate_heatmap(days=30)
print(f"🔥 Heatmapa: {heatmap_path}")

# 4. Wykres kołowy
pie_data = {
    "HTML": 45,
    "CSS": 25,
    "JavaScript": 20,
    "Obrazy": 10
}
pie_path = vm.generate_pie_chart(
    data=pie_data,
    title="Rozkład typów plików"
)
print(f"🥧 Wykres kołowy: {pie_path}")

# 5. Wykres słupkowy
categories = ["Styczeń", "Luty", "Marzec", "Kwiecień"]
values = [12, 19, 15, 22]
bar_path = vm.generate_bar_chart(
    categories=categories,
    values=values,
    title="Aktualizacje per miesiąc"
)
print(f"📊 Wykres słupkowy: {bar_path}")

# Wyczyść cache
vm.clear_cache()
```

### Metody

| Metoda | Opis |
|--------|------|
| `generate_trend_chart()` | Wykres trendów |
| `generate_heatmap()` | Heatmapa aktywności |
| `generate_pie_chart()` | Wykres kołowy |
| `generate_bar_chart()` | Wykres słupkowy |
| `clear_cache()` | Wyczyść cache wykresów |

### Typy wykresów

1. **Line Chart** - trendy w czasie
2. **Heatmap** - aktywność (dni x godziny)
3. **Pie Chart** - rozkład procentowy
4. **Bar Chart** - porównania kategorii

---

## 🔧 Integracja z główną aplikacją

### Dodanie do GUI (gui_modern.py)

```python
# Import nowych modułów
from snapshot_manager import SnapshotManager
from keyboard_shortcuts import KeyboardShortcutsManager
from multi_repository_manager import MultiRepositoryManager
from visualization_manager import VisualizationManager

class ModernGUI:
    def __init__(self, root):
        # ...existing code...
        
        # Inicjalizacja nowych managerów
        self.snapshot_manager = SnapshotManager()
        self.shortcuts_manager = KeyboardShortcutsManager(root)
        self.repo_manager = MultiRepositoryManager()
        self.viz_manager = VisualizationManager(self.db_manager)
        
        # Zarejestruj skróty
        self._setup_keyboard_shortcuts()
        
    def _setup_keyboard_shortcuts(self):
        """Konfiguracja skrótów klawiaturowych"""
        self.shortcuts_manager.register_callback('start_update', self.start_update)
        self.shortcuts_manager.register_callback('open_settings', self.show_settings)
        self.shortcuts_manager.register_callback('show_history', self.show_history_tab)
        # ...more callbacks...
        self.shortcuts_manager.bind_all_shortcuts()
```

---

## 📦 Wymagania

Wszystkie nowe moduły wymagają pakietów z `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Nowe zależności (v5.3.0):**
- `matplotlib>=3.7.0`
- `plotly>=5.14.0`
- `kaleido>=0.2.1`
- `numpy>=1.24.0`
- `pandas>=2.0.0`

---

## 🧪 Testy

Każdy moduł zawiera sekcję `if __name__ == "__main__":` z przykładami użycia.

**Testowanie modułów:**

```bash
# Snapshot Manager
python src/snapshot_manager.py

# Keyboard Shortcuts
python src/keyboard_shortcuts.py

# Multi Repository Manager
python src/multi_repository_manager.py

# Visualization Manager
python src/visualization_manager.py
```

---

## 📝 Konfiguracja

Moduły używają plików konfiguracyjnych w folderze `config/`:

```
config/
├── shortcuts.json          # Skróty klawiaturowe
├── repositories.json       # Repozytoria
└── snapshots_metadata.json # Metadata snapshotów
```

---

## 🔗 Powiązania

```
apk.py
  └─ gui_modern.py
       ├─ snapshot_manager.py
       ├─ keyboard_shortcuts.py
       ├─ multi_repository_manager.py
       └─ visualization_manager.py
            ├─ database_manager.py
            └─ report_generator.py
```

---

## 💡 Wskazówki

1. **Snapshots** - Twórz snapshot przed każdą dużą aktualizacją
2. **Shortcuts** - Dostosuj skróty do swoich potrzeb
3. **Repositories** - Ustaw zależności dla poprawnej kolejności
4. **Visualizations** - Używaj plotly dla interaktywnych wykresów

---

**Wersja:** 5.3.0  
**Data:** 2025-11-18  
**Autor:** Igor Staręga

