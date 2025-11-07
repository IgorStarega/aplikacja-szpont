#!/usr/bin/env python3
"""
Theme Manager - zarządzanie motywami Dark/Light
WERSJA 4.0-alpha (NOWE!)

Obsługuje:
- Automatyczne wykrywanie preferencji systemu (darkdetect)
- Manualny wybór Dark/Light Mode
- Zapisywanie preferencji użytkownika
- Aplicowanie kolorów do GUI
"""

import customtkinter as ctk
import darkdetect
from typing import Dict, Any, Optional
import json
from pathlib import Path


class ThemeManager:
    """Manager motywów aplikacji - Dark/Light Mode"""

    # Kolory dla Light Mode
    LIGHT_THEME = {
        "fg_color": "#f0f0f0",           # Tło
        "text": "#000000",               # Tekst
        "button_fg": "#e0e0e0",          # Tło przycisku
        "button_text": "#000000",        # Tekst przycisku
        "entry_fg": "#ffffff",           # Tło pola
        "entry_text": "#000000",         # Tekst pola
        "frame_fg": "#f5f5f5",          # Tło frame'u
        "accent": "#0078d4",             # Kolor akcentu
    }

    # Kolory dla Dark Mode
    DARK_THEME = {
        "fg_color": "#1e1e1e",           # Tło
        "text": "#ffffff",               # Tekst
        "button_fg": "#2d2d2d",          # Tło przycisku
        "button_text": "#ffffff",        # Tekst przycisku
        "entry_fg": "#3d3d3d",           # Tło pola
        "entry_text": "#ffffff",         # Tekst pola
        "frame_fg": "#252525",           # Tło frame'u
        "accent": "#0084ff",             # Kolor akcentu
    }

    def __init__(self, config_file: str = "config/theme_config.json"):
        """
        Inicjalizacja Theme Manager'a

        Args:
            config_file: Ścieżka do pliku konfiguracji motywu
        """
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(exist_ok=True)

        # Załaduj preferencje użytkownika
        self.theme_mode = self._load_theme_preference()

        # Ustaw motyw systemowy (customtkinter)
        ctk.set_appearance_mode(self.theme_mode)
        # Użyj "blue" jako domyślny theme (customtkinter wymaga konkretnej nazwy)
        ctk.set_default_color_theme("blue")

    def _load_theme_preference(self) -> str:
        """
        Załaduj preferencje motywu z pliku lub automatycznie (NOWE v4.0)

        Returns:
            "dark" lub "light"
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get("theme", "system")
            except Exception:
                pass

        # Jeśli nie ma pliku lub błąd - użyj motywu systemowego
        return self._detect_system_theme()

    def _detect_system_theme(self) -> str:
        """
        Automatycznie wykryj motyw systemowy (NOWE v4.0)

        Returns:
            "dark" jeśli system ma dark mode, inaczej "light"
        """
        try:
            if darkdetect.isDark():
                return "dark"
            else:
                return "light"
        except Exception:
            return "light"  # Domyślnie light jeśli nie można wykryć

    def _save_theme_preference(self) -> None:
        """
        Zapisz preferencję motywu do pliku (NOWE v4.0)
        """
        try:
            config = {"theme": self.theme_mode}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Błąd przy zapisywaniu preferencji motywu: {e}")

    def toggle_theme(self) -> str:
        """
        Przełącz między Dark a Light mode (NOWE v4.0)

        Returns:
            Nowy motyw ("dark" lub "light")
        """
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        ctk.set_appearance_mode(self.theme_mode)
        self._save_theme_preference()
        return self.theme_mode

    def set_theme(self, theme: str) -> None:
        """
        Ustaw motyw (NOWE v4.0)

        Args:
            theme: "dark" lub "light"
        """
        if theme not in ["dark", "light", "system"]:
            raise ValueError(f"Nieznany motyw: {theme}")

        self.theme_mode = theme
        ctk.set_appearance_mode(theme)
        self._save_theme_preference()

    def get_theme(self) -> str:
        """
        Pobierz aktualny motyw (NOWE v4.0)

        Returns:
            Aktualny motyw
        """
        return self.theme_mode

    def get_colors(self) -> Dict[str, str]:
        """
        Pobierz kolory dla aktualnego motywu (NOWE v4.0)

        Returns:
            Dict z kolorami
        """
        return self.DARK_THEME if self.theme_mode == "dark" else self.LIGHT_THEME

    def get_color(self, key: str, default: str = "#ffffff") -> str:
        """
        Pobierz jeden kolor (NOWE v4.0)

        Args:
            key: Klucz koloru
            default: Wartość domyślna

        Returns:
            Kod koloru
        """
        colors = self.get_colors()
        return colors.get(key, default)

