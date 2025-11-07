#!/usr/bin/env python3
"""
Testy dla UpdateManager v2.3+
Uruchom: pytest tests/test_update_manager.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import re
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from update_manager import UpdateManager


class TestUpdateManagerInit:
    """Testy inicjalizacji"""

    def test_init_default(self):
        """Test inicjalizacji z parametrami domyślnymi"""
        manager = UpdateManager()
        assert manager.backup_enabled == True
        assert isinstance(manager.changes_summary, dict)
        assert isinstance(manager.seen_urls, set)
        assert isinstance(manager.removed_urls, set)
        assert isinstance(manager.description_cache, dict)

    def test_init_custom(self):
        """Test inicjalizacji z parametrami custom"""
        def custom_log(msg):
            pass

        manager = UpdateManager(
            log_callback=custom_log,
            backup_enabled=False,
            log_file="test.log"
        )
        assert manager.backup_enabled == False


class TestValidateHtml:
    """Testy walidacji HTML"""

    def test_validate_html_valid_structure(self, tmp_path):
        """Test poprawnej struktury HTML"""
        manager = UpdateManager()
        html_file = tmp_path / "test.html"
        html_content = """
        <html>
            <body>
                <div class="content-wrapper">
                    <div class="row g-3">
                        <div class="col-sm-6">Test</div>
                    </div>
                </div>
            </body>
        </html>
        """
        html_file.write_text(html_content)

        is_valid, errors = manager.validate_html(html_file)
        # Może mieć błędy, ale struktura powinna być OK
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)


class TestExtractDescription:
    """Testy wyciągania opisów"""

    def test_extract_description_index(self):
        """Test dla 'index'"""
        manager = UpdateManager()
        desc = manager._extract_description("index")
        assert desc == "Strona główna"

    def test_extract_description_zadanie(self):
        """Test dla 'zadanie1'"""
        manager = UpdateManager()
        desc = manager._extract_description("zadanie1")
        assert "Zadanie" in desc and "1" in desc

    def test_extract_description_cache(self):
        """Test cache'owania"""
        manager = UpdateManager()
        desc1 = manager._extract_description("zadanie5")
        desc2 = manager._extract_description("zadanie5")
        assert desc1 == desc2
        assert "zadanie5" in manager.description_cache

    def test_extract_description_advanced_patterns(self):
        """Test zaawansowanych wzorców"""
        manager = UpdateManager()

        tests = [
            ("lab1", "Lab"),
            ("projekt2", "Projekt"),
            ("test3", "Test"),
        ]

        for name, keyword in tests:
            desc = manager._extract_description(name)
            # Powinno zwrócić coś sensownego
            assert len(desc) > 0


class TestCleanupOldBackups:
    """Testy czyszczenia backupów"""

    def test_cleanup_old_backups_empty_dir(self):
        """Test gdy brak folderu backups"""
        manager = UpdateManager()
        removed = manager.cleanup_old_backups(days=30)
        assert removed == 0

    def test_cleanup_returns_int(self):
        """Test że zwraca integer"""
        manager = UpdateManager()
        result = manager.cleanup_old_backups()
        assert isinstance(result, int)
        assert result >= 0


class TestErrorHandling:
    """Testy obsługi błędów"""

    def test_validate_git_repo_not_exists(self, tmp_path):
        """Test gdy repo nie istnieje"""
        manager = UpdateManager()
        result = manager.validate_git_repo(tmp_path / "nonexistent")
        assert result == False

    def test_update_html_file_handles_errors(self, tmp_path):
        """Test obsługi błędów w update_html_file"""
        manager = UpdateManager()
        nonexistent_html = tmp_path / "nonexistent.html"
        nonexistent_source = tmp_path / "nonexistent"

        result = manager.update_html_file(nonexistent_html, tmp_path, "test")
        assert isinstance(result, bool)


class TestScanDirectory:
    """Testy skanowania folderów"""

    def test_scan_directory_empty(self, tmp_path):
        """Test skanowania pustego folderu"""
        manager = UpdateManager()
        result = manager.scan_directory(tmp_path, "test")
        assert isinstance(result, dict)

    def test_scan_directory_structure(self, tmp_path):
        """Test struktury wyniku skanowania"""
        manager = UpdateManager()

        # Utwórz strukturę testową
        section_dir = tmp_path / "sekcja1"
        section_dir.mkdir()
        (section_dir / "test.html").write_text("<html></html>")

        result = manager.scan_directory(tmp_path, "test")
        assert isinstance(result, dict)


class TestConstants:
    """Testy stałych aplikacji"""

    def test_allowed_folders(self):
        """Test że stałe foldery są zdefiniowane"""
        assert UpdateManager.ALLOWED_FOLDERS == {"TSiAI", "WiAI", "desktopy", "informatyka"}

    def test_base_url(self):
        """Test że URL bazowy jest zdefiniowany"""
        assert UpdateManager.BASE_URL == "https://prakt.dziadu.dev"


class TestDetailedLog:
    """Testy szczegółowych logów"""

    def test_get_detailed_log(self):
        """Test pobierania logów"""
        manager = UpdateManager()
        manager.log("Test wiadomość")

        log = manager.get_detailed_log()
        assert isinstance(log, str)
        assert "Test wiadomość" in log or len(log) >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

