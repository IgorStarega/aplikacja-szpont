import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple
import os
from dotenv import load_dotenv

class ConfigManager:
    """Menedżer konfiguracji aplikacji"""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)

        # Załaduj zmienne środowiskowe z .env (NOWE v4.0)
        self._load_env_file()

        self.config = self._load_config()

    def _load_env_file(self) -> None:
        """Załadowanie zmiennych z .env (NOWE v4.0)"""
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)

    def _load_config(self) -> Dict[str, Any]:
        """Załadowanie konfiguracji z pliku"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Błąd przy wczytywaniu konfiguracji: {e}")
                return self._get_default_config()
        return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Domyślna konfiguracja (z priorytetem na .env)"""
        # Wpisane domyślnie lokalne ścieżki repozytoriów
        return {
            # Pobierz z .env jeśli istnieje, inaczej użyj lokalnych ścieżek
            "source_path": os.getenv("SOURCE_REPO_PATH", r"C:\Users\stare\szkola25-26"),
            "target_path": os.getenv("TARGET_REPO_PATH", r"C:\Users\stare\strona dziadu-dev"),
            "auto_update_enabled": os.getenv("AUTO_UPDATE_ENABLED", "false").lower() == "true",
            "auto_update_interval": int(os.getenv("AUTO_UPDATE_INTERVAL", "60")),
            "auto_update_interval_unit": os.getenv("AUTO_UPDATE_INTERVAL_UNIT", "minutes"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "backup_enabled": os.getenv("BACKUP_ENABLED", "true").lower() == "true",
            "backup_cleanup_days": int(os.getenv("BACKUP_CLEANUP_DAYS", "30")),
            "last_update": None,
            "update_history": []
        }

    def get_from_env(self, key: str, default: Any = None) -> Any:
        """
        Pobiera wartość ze zmiennych środowiskowych (NOWE v4.0)

        Args:
            key: Nazwa zmiennej środowiskowej
            default: Wartość domyślna

        Returns:
            Wartość ze zmiennej środowiskowej lub domyślna
        """
        return os.getenv(key, default)

    def save_config(self):
        """Zapisanie konfiguracji do pliku"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Błąd przy zapisywaniu konfiguracji: {e}")

    def get(self, key: str, default=None) -> Any:
        """Pobranie wartości konfiguracji"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Ustawienie wartości konfiguracji"""
        self.config[key] = value
        self.save_config()

    def add_update_history(self, summary: Dict[str, Any]):
        """Dodanie wpisu do historii aktualizacji"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "added_count": len(summary.get("added", [])),
            "modified_count": len(summary.get("modified", [])),
            "removed_count": len(summary.get("removed", [])),
            "folders": summary.get("folders_updated", [])
        }

        history = self.config.get("update_history", [])
        history.append(history_entry)

        # Przechowuj ostatnie 50 aktualizacji
        if len(history) > 50:
            history = history[-50:]

        self.config["update_history"] = history
        self.config["last_update"] = datetime.now().isoformat()
        self.save_config()

    def get_update_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Pobranie historii aktualizacji"""
        history = self.config.get("update_history", [])
        return history[-limit:]

    def validate_config(self) -> Tuple[bool, List[str]]:
        """
        ⭐ NOWE: Waliduje konfigurację

        Returns:
            (is_valid, errors) - czy konfiguracja jest ważna i lista błędów
        """
        required_fields = ["source_path", "target_path"]
        errors = []

        try:
            config_data = self.config

            # Sprawdzenie wymaganych pól
            for field in required_fields:
                if field not in config_data or not config_data[field]:
                    errors.append(f"Brakuje wymaganego pola: {field}")

            # Walidacja ścieżek
            if "source_path" in config_data:
                source_path = Path(config_data["source_path"])
                if not source_path.exists():
                    errors.append(f"Ścieżka nie istnieje: {config_data['source_path']}")

            if "target_path" in config_data:
                target_path = Path(config_data["target_path"])
                if not target_path.exists():
                    errors.append(f"Ścieżka nie istnieje: {config_data['target_path']}")

            # Walidacja typów
            if "auto_update_interval" in config_data:
                if not isinstance(config_data["auto_update_interval"], int):
                    errors.append("auto_update_interval musi być liczbą")

            is_valid = len(errors) == 0
            return is_valid, errors

        except Exception as e:
            errors.append(f"Błąd walidacji konfiguracji: {str(e)}")
            return False, errors
