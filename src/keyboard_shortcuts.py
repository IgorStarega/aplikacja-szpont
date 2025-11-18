"""
Keyboard Shortcuts Manager dla Aktualizatora Strony v5.3.0
Obsługa skrótów klawiaturowych i quick actions

Funkcje:
- Globalne skróty klawiaturowe
- Kontekstowe menu (prawy przycisk myszy)
- Customizowalne kombinacje klawiszy
- Export/import mappings
"""

from typing import Dict, Callable, List, Optional
import json
from pathlib import Path


class KeyboardShortcutsManager:
    """Zarządzanie skrótami klawiaturowymi"""

    # Domyślne skróty
    DEFAULT_SHORTCUTS = {
        # Główne akcje
        '<Control-u>': 'start_update',
        '<Control-U>': 'start_update',
        '<Control-s>': 'open_settings',
        '<Control-S>': 'open_settings',
        '<Control-h>': 'show_history',
        '<Control-H>': 'show_history',
        '<Control-r>': 'refresh_view',
        '<Control-R>': 'refresh_view',
        '<F5>': 'refresh_view',

        # Wyszukiwanie
        '<Control-f>': 'search_history',
        '<Control-F>': 'search_history',

        # Snapshots
        '<Control-n>': 'new_snapshot',
        '<Control-N>': 'new_snapshot',
        '<Control-b>': 'manage_backups',
        '<Control-B>': 'manage_backups',

        # Motywy
        '<Control-t>': 'toggle_theme',
        '<Control-T>': 'toggle_theme',

        # Nawigacja zakładek
        '<Control-1>': 'tab_main',
        '<Control-2>': 'tab_analytics',
        '<Control-3>': 'tab_scheduler',
        '<Control-4>': 'tab_settings',
        '<Control-5>': 'tab_about',

        # Aplikacja
        '<Control-q>': 'quit_app',
        '<Control-Q>': 'quit_app',
        '<Alt-F4>': 'quit_app',

        # Help
        '<F1>': 'show_help',

        # Debug (jeśli enabled)
        '<Control-d>': 'toggle_debug',
        '<Control-D>': 'toggle_debug',
    }

    def __init__(self, root, config_path: Path = None):
        """
        Inicjalizacja Keyboard Shortcuts Manager

        Args:
            root: Tkinter root window
            config_path: Ścieżka do pliku konfiguracji skrótów
        """
        self.root = root
        self.config_path = config_path or Path.cwd() / "config" / "shortcuts.json"
        self.shortcuts: Dict[str, str] = {}
        self.callbacks: Dict[str, Callable] = {}
        self.bindings: List = []

        # Wczytaj konfigurację lub użyj domyślnej
        self._load_shortcuts()

    def _load_shortcuts(self):
        """Wczytaj skróty z pliku lub użyj domyślnych"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.shortcuts = json.load(f)
            except Exception as e:
                print(f"⚠️  Błąd wczytywania shortcuts: {e}, używam domyślnych")
                self.shortcuts = self.DEFAULT_SHORTCUTS.copy()
        else:
            self.shortcuts = self.DEFAULT_SHORTCUTS.copy()
            self._save_shortcuts()

    def _save_shortcuts(self):
        """Zapisz skróty do pliku"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.shortcuts, f, indent=2)

    def register_callback(self, action_name: str, callback: Callable):
        """
        Zarejestruj callback dla akcji

        Args:
            action_name: Nazwa akcji (np. 'start_update')
            callback: Funkcja do wywołania
        """
        self.callbacks[action_name] = callback

    def bind_all_shortcuts(self):
        """Binduj wszystkie skróty do okna"""
        # Usuń poprzednie bindowania
        self.unbind_all()

        # Binduj nowe
        for key_combo, action_name in self.shortcuts.items():
            if action_name in self.callbacks:
                binding = self.root.bind(
                    key_combo,
                    lambda event, action=action_name: self._execute_action(action)
                )
                self.bindings.append((key_combo, binding))

    def unbind_all(self):
        """Usuń wszystkie bindowania"""
        for key_combo, _ in self.bindings:
            try:
                self.root.unbind(key_combo)
            except:
                pass
        self.bindings.clear()

    def _execute_action(self, action_name: str):
        """Wykonaj akcję związaną ze skrótem"""
        callback = self.callbacks.get(action_name)
        if callback:
            try:
                callback()
            except Exception as e:
                print(f"❌ Błąd wykonywania akcji '{action_name}': {e}")
        else:
            print(f"⚠️  Brak callbacka dla akcji: {action_name}")

    def add_shortcut(self, key_combo: str, action_name: str):
        """
        Dodaj nowy skrót

        Args:
            key_combo: Kombinacja klawiszy (np. '<Control-x>')
            action_name: Nazwa akcji
        """
        self.shortcuts[key_combo] = action_name
        self._save_shortcuts()
        self.bind_all_shortcuts()

    def remove_shortcut(self, key_combo: str):
        """Usuń skrót"""
        if key_combo in self.shortcuts:
            del self.shortcuts[key_combo]
            self._save_shortcuts()
            self.bind_all_shortcuts()

    def get_shortcut_for_action(self, action_name: str) -> Optional[str]:
        """Pobierz skrót dla akcji"""
        for key_combo, action in self.shortcuts.items():
            if action == action_name:
                return key_combo
        return None

    def get_all_shortcuts(self) -> Dict[str, str]:
        """Pobierz wszystkie skróty"""
        return self.shortcuts.copy()

    def reset_to_defaults(self):
        """Resetuj do domyślnych skrótów"""
        self.shortcuts = self.DEFAULT_SHORTCUTS.copy()
        self._save_shortcuts()
        self.bind_all_shortcuts()

    def get_shortcuts_help_text(self) -> str:
        """Generuj tekst pomocy ze skrótami"""
        help_text = "⌨️  SKRÓTY KLAWIATUROWE\n"
        help_text += "=" * 50 + "\n\n"

        # Grupuj skróty
        groups = {
            "Główne akcje": ['start_update', 'open_settings', 'show_history', 'refresh_view'],
            "Wyszukiwanie": ['search_history'],
            "Snapshots": ['new_snapshot', 'manage_backups'],
            "Motywy": ['toggle_theme'],
            "Nawigacja": ['tab_main', 'tab_analytics', 'tab_scheduler', 'tab_settings', 'tab_about'],
            "Aplikacja": ['quit_app', 'show_help'],
        }

        for group_name, actions in groups.items():
            help_text += f"\n{group_name}:\n"
            help_text += "-" * 30 + "\n"

            for action in actions:
                key = self.get_shortcut_for_action(action)
                if key:
                    # Formatuj nazwę akcji
                    action_display = action.replace('_', ' ').title()
                    key_display = key.replace('<', '').replace('>', '').replace('-', '+')
                    help_text += f"  {key_display:20s} → {action_display}\n"

        return help_text


class QuickActionsMenu:
    """Kontekstowe menu quick actions (PPM)"""

    def __init__(self, parent):
        """
        Inicjalizacja Quick Actions Menu

        Args:
            parent: Widget rodzica
        """
        self.parent = parent
        self.menu = None

    def create_menu(self, widget, actions: Dict[str, Callable]):
        """
        Stwórz menu kontekstowe dla widgeta

        Args:
            widget: Widget do którego przypisać menu
            actions: Dict z nazwami akcji i callbackami
        """
        import tkinter as tk

        self.menu = tk.Menu(widget, tearoff=0)

        for action_name, callback in actions.items():
            if action_name == "separator":
                self.menu.add_separator()
            else:
                self.menu.add_command(label=action_name, command=callback)

        # Bind prawy przycisk myszy
        widget.bind("<Button-3>", self._show_menu)

    def _show_menu(self, event):
        """Pokaż menu w miejscu kliknięcia"""
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def add_action(self, action_name: str, callback: Callable, index: int = None):
        """Dodaj akcję do menu"""
        if index is not None:
            self.menu.insert_command(index, label=action_name, command=callback)
        else:
            self.menu.add_command(label=action_name, command=callback)

    def remove_action(self, index: int):
        """Usuń akcję z menu"""
        self.menu.delete(index)


# ===== PRZYKŁAD UŻYCIA =====
if __name__ == "__main__":
    import tkinter as tk

    # Stwórz okno testowe
    root = tk.Tk()
    root.title("Keyboard Shortcuts Test")
    root.geometry("600x400")

    # Inicjalizacja managera
    shortcuts_manager = KeyboardShortcutsManager(root)

    # Zarejestruj przykładowe callbacki
    def start_update():
        print("🚀 Rozpoczynam aktualizację...")

    def open_settings():
        print("⚙️  Otwieram ustawienia...")

    def show_help():
        print(shortcuts_manager.get_shortcuts_help_text())

    shortcuts_manager.register_callback('start_update', start_update)
    shortcuts_manager.register_callback('open_settings', open_settings)
    shortcuts_manager.register_callback('show_help', show_help)

    # Binduj skróty
    shortcuts_manager.bind_all_shortcuts()

    # Label z informacjami
    info_label = tk.Label(
        root,
        text="Wypróbuj skróty klawiaturowe:\n\n"
             "Ctrl+U - Rozpocznij aktualizację\n"
             "Ctrl+S - Ustawienia\n"
             "F1 - Pomoc",
        font=("Arial", 12),
        justify="left"
    )
    info_label.pack(pady=50)

    # Quick Actions Menu
    text_widget = tk.Text(root, height=10, width=50)
    text_widget.pack(pady=20)

    quick_actions = QuickActionsMenu(root)
    quick_actions.create_menu(text_widget, {
        "Kopiuj": lambda: print("Copy"),
        "Wklej": lambda: print("Paste"),
        "separator": None,
        "Wyczyść": lambda: text_widget.delete("1.0", "end"),
    })

    root.mainloop()

