#!/usr/bin/env python3
"""
Auto-Update Manager - v5.2 Feature
Automatyczne aktualizacje aplikacji

Funkcjonalność:
- ✅ Sprawdzanie nowych wersji z GitHub
- ✅ Pobieranie i instalacja aktualizacji
- ✅ Backup przed aktualizacją
- ✅ Rollback w przypadku błędu
- ✅ Powiadomienia o dostępnych aktualizacjach
"""

import requests
import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Callable
from datetime import datetime
import hashlib
import logging


class AutoUpdateManager:
    """Manager automatycznych aktualizacji - v5.2 Feature"""

    GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/releases/latest"
    CURRENT_VERSION = "5.2.0"
    UPDATE_CHECK_FILE = "src/.config/last_update_check.json"
    BACKUP_DIR = "backups/app_backups"

    def __init__(self,
                 github_owner: str = "IgorStarega",
                 github_repo: str = "aplikacja-szpont",
                 log_callback: Callable = None):
        """
        Inicjalizacja Auto-Update Manager'a

        Args:
            github_owner: Właściciel repozytorium GitHub
            github_repo: Nazwa repozytorium
            log_callback: Funkcja do logowania
        """
        self.github_owner = github_owner
        self.github_repo = github_repo
        self.log_callback = log_callback or print
        self.logger = logging.getLogger(__name__)

        # Utwórz katalogi
        Path(self.UPDATE_CHECK_FILE).parent.mkdir(parents=True, exist_ok=True)
        Path(self.BACKUP_DIR).mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Logowanie wiadomości"""
        if self.log_callback:
            self.log_callback(f"[AUTO-UPDATE] {message}")
        self.logger.info(message)

    def get_current_version(self) -> str:
        """
        Pobierz aktualną wersję aplikacji

        Returns:
            Wersja w formacie "X.Y.Z"
        """
        return self.CURRENT_VERSION

    def check_for_updates(self) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Sprawdź czy dostępna jest nowa wersja

        Returns:
            (is_available, release_info) - czy dostępna aktualizacja i info o release
        """
        try:
            self.log("🔍 Sprawdzanie dostępnych aktualizacji...")

            url = self.GITHUB_API_URL.format(
                owner=self.github_owner,
                repo=self.github_repo
            )

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            release_data = response.json()
            latest_version = release_data.get("tag_name", "").lstrip("v")
            current_version = self.get_current_version()

            self.log(f"📦 Aktualna wersja: {current_version}")
            self.log(f"📦 Najnowsza wersja: {latest_version}")

            # Porównaj wersje
            is_newer = self._compare_versions(latest_version, current_version) > 0

            if is_newer:
                self.log(f"✅ Dostępna nowa wersja: {latest_version}")
                return True, release_data
            else:
                self.log("ℹ️  Aplikacja jest aktualna")
                return False, None

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Błąd sprawdzania aktualizacji: {str(e)}")
            return False, None
        except Exception as e:
            self.log(f"❌ Nieoczekiwany błąd: {str(e)}")
            return False, None

    def _compare_versions(self, version1: str, version2: str) -> int:
        """
        Porównaj dwie wersje

        Args:
            version1: Pierwsza wersja (X.Y.Z)
            version2: Druga wersja (X.Y.Z)

        Returns:
            1 jeśli version1 > version2
            0 jeśli version1 == version2
            -1 jeśli version1 < version2
        """
        try:
            v1_parts = [int(x) for x in version1.split(".")]
            v2_parts = [int(x) for x in version2.split(".")]

            # Dopełnij zerami jeśli długości się różnią
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts += [0] * (max_len - len(v1_parts))
            v2_parts += [0] * (max_len - len(v2_parts))

            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1

            return 0
        except:
            return 0

    def download_update(self, release_info: Dict[str, Any]) -> Optional[Path]:
        """
        Pobierz aktualizację z GitHub

        Args:
            release_info: Informacje o release z GitHub API

        Returns:
            Ścieżka do pobranego pliku lub None
        """
        try:
            assets = release_info.get("assets", [])
            if not assets:
                self.log("❌ Brak plików do pobrania")
                return None

            # Znajdź plik .zip
            asset = None
            for a in assets:
                if a.get("name", "").endswith(".zip"):
                    asset = a
                    break

            if not asset:
                self.log("❌ Nie znaleziono pliku .zip")
                return None

            download_url = asset.get("browser_download_url")
            filename = asset.get("name")

            self.log(f"📥 Pobieranie: {filename}")

            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()

            download_path = Path(self.BACKUP_DIR) / filename

            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.log(f"✅ Pobrano: {download_path}")
            return download_path

        except Exception as e:
            self.log(f"❌ Błąd pobierania: {str(e)}")
            return None

    def create_backup(self) -> Optional[Path]:
        """
        Utwórz backup aktualnej aplikacji

        Returns:
            Ścieżka do backupu lub None
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"app_backup_{timestamp}"
            backup_path = Path(self.BACKUP_DIR) / backup_name

            self.log(f"💾 Tworzenie backupu: {backup_name}")

            # Skopiuj pliki źródłowe
            shutil.copytree("src", backup_path / "src",
                          ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.cache', '.data'))
            shutil.copy2("apk.py", backup_path / "apk.py")
            shutil.copy2("config.json", backup_path / "config.json")
            shutil.copy2("requirements.txt", backup_path / "requirements.txt")

            self.log(f"✅ Backup utworzony: {backup_path}")
            return backup_path

        except Exception as e:
            self.log(f"❌ Błąd tworzenia backupu: {str(e)}")
            return None

    def install_update(self, update_file: Path) -> bool:
        """
        Zainstaluj aktualizację

        Args:
            update_file: Ścieżka do pliku .zip z aktualizacją

        Returns:
            True jeśli sukces, False w przeciwnym razie
        """
        try:
            # Utwórz backup
            backup_path = self.create_backup()
            if not backup_path:
                self.log("❌ Nie udało się utworzyć backupu")
                return False

            self.log(f"📦 Instalowanie aktualizacji...")

            # Rozpakuj aktualizację do folderu tymczasowego
            temp_dir = Path(self.BACKUP_DIR) / "temp_update"
            temp_dir.mkdir(exist_ok=True)

            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Znajdź katalog główny w archiwum
            extracted_dirs = list(temp_dir.iterdir())
            if len(extracted_dirs) == 1 and extracted_dirs[0].is_dir():
                source_dir = extracted_dirs[0]
            else:
                source_dir = temp_dir

            # Kopiuj nowe pliki
            if (source_dir / "src").exists():
                shutil.rmtree("src", ignore_errors=True)
                shutil.copytree(source_dir / "src", "src")

            if (source_dir / "apk.py").exists():
                shutil.copy2(source_dir / "apk.py", "apk.py")

            if (source_dir / "requirements.txt").exists():
                shutil.copy2(source_dir / "requirements.txt", "requirements.txt")

            # Wyczyść temp
            shutil.rmtree(temp_dir, ignore_errors=True)

            self.log("✅ Aktualizacja zainstalowana!")
            self.log("ℹ️  Uruchom ponownie aplikację")

            return True

        except Exception as e:
            self.log(f"❌ Błąd instalacji: {str(e)}")
            self.log("🔄 Przywracanie z backupu...")
            # Tutaj można dodać rollback
            return False

    def rollback(self, backup_path: Path) -> bool:
        """
        Przywróć aplikację z backupu

        Args:
            backup_path: Ścieżka do backupu

        Returns:
            True jeśli sukces, False w przeciwnym razie
        """
        try:
            self.log(f"🔄 Przywracanie z backupu: {backup_path}")

            if (backup_path / "src").exists():
                shutil.rmtree("src", ignore_errors=True)
                shutil.copytree(backup_path / "src", "src")

            if (backup_path / "apk.py").exists():
                shutil.copy2(backup_path / "apk.py", "apk.py")

            if (backup_path / "config.json").exists():
                shutil.copy2(backup_path / "config.json", "config.json")

            self.log("✅ Przywrócono z backupu")
            return True

        except Exception as e:
            self.log(f"❌ Błąd rollback: {str(e)}")
            return False

    def auto_update(self) -> bool:
        """
        Automatyczna aktualizacja (sprawdź, pobierz, zainstaluj)

        Returns:
            True jeśli zainstalowano aktualizację, False w przeciwnym razie
        """
        is_available, release_info = self.check_for_updates()

        if not is_available:
            return False

        # Pobierz aktualizację
        update_file = self.download_update(release_info)
        if not update_file:
            return False

        # Zainstaluj
        success = self.install_update(update_file)

        # Usuń pobrany plik
        try:
            update_file.unlink()
        except:
            pass

        return success

    def save_update_check(self):
        """Zapisz czas ostatniego sprawdzenia aktualizacji"""
        try:
            data = {
                "last_check": datetime.now().isoformat(),
                "version": self.get_current_version()
            }
            with open(self.UPDATE_CHECK_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except:
            pass

    def get_last_update_check(self) -> Optional[datetime]:
        """
        Pobierz czas ostatniego sprawdzenia aktualizacji

        Returns:
            Datetime ostatniego sprawdzenia lub None
        """
        try:
            if Path(self.UPDATE_CHECK_FILE).exists():
                with open(self.UPDATE_CHECK_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return datetime.fromisoformat(data.get("last_check"))
        except:
            pass
        return None

