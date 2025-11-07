# 📖 API Reference - UpdateManager v2.2

## Przegląd Klasy

```python
class UpdateManager:
    """Manager aktualizacji zawartości HTML dla strony prakt.dziadu.dev"""
```

## Konstruktor

### `__init__(log_callback, backup_enabled, log_file)`

Inicjalizuje manager.

**Parametry:**
- `log_callback` (Callable): Funkcja do logowania (domyślnie: print)
- `backup_enabled` (bool): Czy tworzyć backupy (domyślnie: True)
- `log_file` (str, optional): Ścieżka do pliku logów

**Przykład:**
```python
manager = UpdateManager(
    log_callback=print,
    backup_enabled=True,
    log_file="logs/update.log"
)
```

---

## Metody Publiczne

### `validate_git_repo(path: Path) -> bool`

⭐ NOWE (v2.2) - Waliduje czy ścieżka zawiera repozytorium Git.

**Parametry:**
- `path` (Path): Ścieżka do sprawdzenia

**Zwraca:**
- `True` jeśli to repozytorium Git
- `False` jeśli nie

**Przykład:**
```python
if manager.validate_git_repo(Path("C:/repo")):
    print("Repozytorium jest dostępne")
```

---

### `pull_repo(path: Path) -> bool`

Pobiera zmiany z repozytorium Git.

**Parametry:**
- `path` (Path): Ścieżka do repozytorium

**Zwraca:**
- `True` jeśli powodzenie
- `False` jeśli błąd

---

### `create_backup(html_path: Path) -> Optional[Path]`

⭐ NOWE (v2.2) - Tworzy backup pliku HTML.

**Parametry:**
- `html_path` (Path): Ścieżka do pliku HTML

**Zwraca:**
- Ścieżka do backupu lub None jeśli się nie powiodło

**Przykład:**
```python
backup = manager.create_backup(Path("desktopy.html"))
if backup:
    print(f"Backup: {backup}")
```

---

### `scan_directory(folder_path: Path, folder_name: str) -> Dict`

Skanuje folder hierarchicznie i buduje strukturę zadań.

**Parametry:**
- `folder_path` (Path): Ścieżka do folderu
- `folder_name` (str): Nazwa kategorii (desktopy, TSiAI, itp.)

**Zwraca:**
- Słownik struktury zadań

**Struktura zwracana:**
```python
{
    "sekcja_1": [
        {"title": "...", "url": "...", "description": "..."},
        {"type": "subsection", "name": "...", "tasks": [...]}
    ]
}
```

---

### `update_html_file(html_path: Path, source_path: Path, folder_name: str) -> bool`

Aktualizuje plik HTML - dodaje nowe karty i usuwa stare.

**Parametry:**
- `html_path` (Path): Ścieżka do pliku HTML
- `source_path` (Path): Ścieżka do repozytorium źródłowego
- `folder_name` (str): Nazwa kategorii

**Zwraca:**
- `True` jeśli powodzenie
- `False` jeśli błąd

**Co robi:**
1. Tworzy backup HTML
2. Skanuje folder źródłowy
3. Dodaje nowe karty
4. Usuwa stare karty (jeśli zadań już nie ma)
5. Zapisuje plik

---

### `remove_obsolete_cards(container, valid_urls: Set[str]) -> int`

⭐ NOWE (v2.2) - Usuwa karty których nie ma w valid_urls.

**Parametry:**
- `container`: BeautifulSoup container
- `valid_urls` (Set[str]): Set prawidłowych URL'ów

**Zwraca:**
- Liczba usuniętych kart

---

### `run_full_update(source_path: Path, target_path: Path) -> bool`

Pełna aktualizacja - całość procesu.

**Parametry:**
- `source_path` (Path): Ścieżka do szkoła25-26
- `target_path` (Path): Ścieżka do strona-dziadu-dev

**Zwraca:**
- `True` jeśli powodzenie
- `False` jeśli błąd

**Proces:**
1. Waliduje repozytoria Git
2. Pobiera zmiany (git pull)
3. Skanuje strukturę
4. Aktualizuje pliki HTML
5. Commituje i pushuje zmiany

**Przykład:**
```python
manager = UpdateManager()
success = manager.run_full_update(
    Path("C:/szkoła25-26"),
    Path("C:/strona-dziadu-dev")
)
if success:
    print("Aktualizacja zakończona pomyślnie!")
```

---

### `commit_and_push(repo_path: Path) -> bool`

Commituje i pushuje zmiany.

**Parametry:**
- `repo_path` (Path): Ścieżka do repozytorium

**Zwraca:**
- `True` jeśli powodzenie
- `False` jeśli błąd

---

### `get_detailed_log() -> str`

⭐ NOWE (v2.2) - Zwraca szczegółowy log zmian.

**Zwraca:**
- String z logiem (każda linia = jedna operacja)

**Przykład:**
```python
log = manager.get_detailed_log()
print(log)  # Wypisze wszystkie operacje
```

---

## Właściwości

### `changes_summary: Dict`

Podsumowanie zmian.

```python
{
    "added": [],           # Nowe karty
    "removed": [],         # Usunięte karty
    "modified": [],        # Zmodyfikowane pliki HTML
    "folders_updated": []  # Zaktualizowane foldery
}
```

### `seen_urls: Set[str]`

Set URL'ów które już są na stronie.

### `removed_urls: Set[str]`

Set URL'ów które zostały usunięte.

### `detailed_log: List[str]`

Lista szczegółowych logów.

---

## Metody Prywatne (dla developerów)

| Metoda | Opis |
|--------|------|
| `_process_section()` | Przetwarza folder sekcji |
| `_process_subsection()` | Przetwarza folder podsekcji |
| `_add_task()` | Dodaje zadanie do struktury |
| `_create_task_info()` | Tworzy info o zadaniu |
| `_extract_description()` | Generuje opis z nazwy |
| `_generate_card_html()` | Generuje HTML karty |
| `_get_existing_urls()` | Pobiera istniejące URLe |
| `_find_and_remove_card()` | Znajduje i usuwa kartę |
| `_add_card_to_html()` | Dodaje kartę do HTML |
| `_create_and_add_section()` | Tworzy nową sekcję |
| `_create_subsection_and_add_card()` | Tworzy podsekcję |
| `_generate_commit_message()` | Generuje wiadomość commita |

---

## Stałe

```python
ALLOWED_FOLDERS = {"TSiAI", "WiAI", "desktopy", "informatyka"}
BASE_URL = "https://prakt.dziadu.dev"
```

---

## Przykład Pełnego Użycia

```python
from src.update_manager import UpdateManager
from pathlib import Path

# Inicjalizacja
manager = UpdateManager(
    log_callback=print,
    backup_enabled=True,
    log_file="logs/update.log"
)

# Ścieżki
source = Path("C:/szkoła25-26")
target = Path("C:/strona-dziadu-dev")

# Walidacja (nowe w 2.2!)
if not manager.validate_git_repo(source):
    print("Błąd: Brak repozytorium źródłowego")
    exit(1)

# Pełna aktualizacja
success = manager.run_full_update(source, target)

# Podsumowanie
if success:
    print(f"Dodane: {manager.changes_summary['added']}")
    print(f"Usunięte: {manager.removed_urls}")
    print("\nLog zmian:")
    print(manager.get_detailed_log())
```

---

**Wersja:** 2.2  
**Ostatnia aktualizacja:** 2025-01-06

