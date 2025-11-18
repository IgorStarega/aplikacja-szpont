"""
Snapshot Manager dla Aktualizatora Strony v5.3.0
Zarządzanie snapshotami, rollback i visual diff

Funkcje:
- Tworzenie manualnych i automatycznych snapshotów
- Rollback do poprzednich stanów
- Visual diff między snapshotami
- Kompresja i metadata
- Export/import snapshotów
"""

import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import difflib


class SnapshotManager:
    """Zarządzanie snapshotami aplikacji"""

    def __init__(self, base_path: Path = None):
        """
        Inicjalizacja Snapshot Manager

        Args:
            base_path: Ścieżka bazowa do folderów (domyślnie: ./snapshots)
        """
        self.base_path = base_path or Path.cwd() / "snapshots"
        self.base_path.mkdir(exist_ok=True)
        self.metadata_file = self.base_path / "snapshots_metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        """Wczytaj metadata snapshotów"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"snapshots": []}

    def _save_metadata(self):
        """Zapisz metadata snapshotów"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

    def create_snapshot(
        self,
        source_path: Path,
        name: str = None,
        description: str = "",
        tags: List[str] = None,
        auto: bool = False
    ) -> Dict:
        """
        Stwórz nowy snapshot

        Args:
            source_path: Ścieżka do folderu do zbackupowania
            name: Nazwa snapshota (domyślnie: timestamp)
            description: Opis snapshota
            tags: Lista tagów
            auto: Czy to automatyczny snapshot

        Returns:
            Dict z informacjami o snapshocie
        """
        timestamp = datetime.now()
        snapshot_name = name or f"snapshot_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        snapshot_path = self.base_path / snapshot_name

        # Kopiuj folder
        if source_path.exists():
            shutil.copytree(source_path, snapshot_path, dirs_exist_ok=True)
        else:
            raise FileNotFoundError(f"Ścieżka źródłowa nie istnieje: {source_path}")

        # Oblicz hash dla weryfikacji
        snapshot_hash = self._calculate_dir_hash(snapshot_path)

        # Metadata
        snapshot_info = {
            "name": snapshot_name,
            "path": str(snapshot_path),
            "timestamp": timestamp.isoformat(),
            "description": description,
            "tags": tags or [],
            "auto": auto,
            "hash": snapshot_hash,
            "size_mb": self._get_dir_size(snapshot_path) / (1024 * 1024)
        }

        self.metadata["snapshots"].append(snapshot_info)
        self._save_metadata()

        return snapshot_info

    def list_snapshots(
        self,
        tag: str = None,
        auto_only: bool = False,
        manual_only: bool = False
    ) -> List[Dict]:
        """
        Lista snapshotów z opcjonalnym filtrowaniem

        Args:
            tag: Filtruj po tagu
            auto_only: Tylko automatyczne
            manual_only: Tylko manualne

        Returns:
            Lista snapshotów
        """
        snapshots = self.metadata["snapshots"]

        if tag:
            snapshots = [s for s in snapshots if tag in s.get("tags", [])]

        if auto_only:
            snapshots = [s for s in snapshots if s.get("auto", False)]

        if manual_only:
            snapshots = [s for s in snapshots if not s.get("auto", False)]

        # Sortuj od najnowszych
        snapshots.sort(key=lambda x: x["timestamp"], reverse=True)

        return snapshots

    def restore_snapshot(self, snapshot_name: str, target_path: Path) -> bool:
        """
        Przywróć snapshot do określonej lokalizacji

        Args:
            snapshot_name: Nazwa snapshota do przywrócenia
            target_path: Ścieżka docelowa

        Returns:
            True jeśli sukces
        """
        # Znajdź snapshot
        snapshot = next(
            (s for s in self.metadata["snapshots"] if s["name"] == snapshot_name),
            None
        )

        if not snapshot:
            raise ValueError(f"Snapshot nie znaleziony: {snapshot_name}")

        snapshot_path = Path(snapshot["path"])

        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot path nie istnieje: {snapshot_path}")

        # Weryfikuj hash
        current_hash = self._calculate_dir_hash(snapshot_path)
        if current_hash != snapshot["hash"]:
            raise ValueError("Hash verification failed! Snapshot może być uszkodzony.")

        # Backup obecnego stanu przed restore (safety)
        if target_path.exists():
            backup_name = f"pre_restore_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.create_snapshot(target_path, name=backup_name, auto=True,
                               description=f"Auto backup before restoring {snapshot_name}")

        # Usuń obecną zawartość
        if target_path.exists():
            shutil.rmtree(target_path)

        # Przywróć snapshot
        shutil.copytree(snapshot_path, target_path)

        return True

    def delete_snapshot(self, snapshot_name: str) -> bool:
        """
        Usuń snapshot

        Args:
            snapshot_name: Nazwa snapshota do usunięcia

        Returns:
            True jeśli sukces
        """
        snapshot = next(
            (s for s in self.metadata["snapshots"] if s["name"] == snapshot_name),
            None
        )

        if not snapshot:
            return False

        # Usuń folder
        snapshot_path = Path(snapshot["path"])
        if snapshot_path.exists():
            shutil.rmtree(snapshot_path)

        # Usuń z metadata
        self.metadata["snapshots"] = [
            s for s in self.metadata["snapshots"] if s["name"] != snapshot_name
        ]
        self._save_metadata()

        return True

    def compare_snapshots(
        self,
        snapshot1_name: str,
        snapshot2_name: str
    ) -> Dict[str, List[str]]:
        """
        Porównaj dwa snapshoty

        Args:
            snapshot1_name: Nazwa pierwszego snapshota
            snapshot2_name: Nazwa drugiego snapshota

        Returns:
            Dict z różnicami (added, removed, modified)
        """
        snap1 = next((s for s in self.metadata["snapshots"] if s["name"] == snapshot1_name), None)
        snap2 = next((s for s in self.metadata["snapshots"] if s["name"] == snapshot2_name), None)

        if not snap1 or not snap2:
            raise ValueError("Jeden lub oba snapshoty nie znalezione")

        path1 = Path(snap1["path"])
        path2 = Path(snap2["path"])

        files1 = set(self._get_all_files(path1))
        files2 = set(self._get_all_files(path2))

        added = list(files2 - files1)
        removed = list(files1 - files2)

        # Sprawdź zmodyfikowane pliki
        common_files = files1 & files2
        modified = []

        for file in common_files:
            file1 = path1 / file
            file2 = path2 / file

            if file1.is_file() and file2.is_file():
                hash1 = self._calculate_file_hash(file1)
                hash2 = self._calculate_file_hash(file2)

                if hash1 != hash2:
                    modified.append(file)

        return {
            "added": sorted(added),
            "removed": sorted(removed),
            "modified": sorted(modified)
        }

    def visual_diff(
        self,
        snapshot1_name: str,
        snapshot2_name: str,
        file_path: str
    ) -> str:
        """
        Pokaż visual diff dla konkretnego pliku

        Args:
            snapshot1_name: Nazwa pierwszego snapshota
            snapshot2_name: Nazwa drugiego snapshota
            file_path: Relatywna ścieżka do pliku

        Returns:
            HTML diff lub unified diff string
        """
        snap1 = next((s for s in self.metadata["snapshots"] if s["name"] == snapshot1_name), None)
        snap2 = next((s for s in self.metadata["snapshots"] if s["name"] == snapshot2_name), None)

        if not snap1 or not snap2:
            raise ValueError("Jeden lub oba snapshoty nie znalezione")

        file1 = Path(snap1["path"]) / file_path
        file2 = Path(snap2["path"]) / file_path

        if not file1.exists() or not file2.exists():
            return "Plik nie istnieje w jednym lub obu snapshotach"

        # Wczytaj zawartość
        with open(file1, 'r', encoding='utf-8', errors='ignore') as f:
            lines1 = f.readlines()

        with open(file2, 'r', encoding='utf-8', errors='ignore') as f:
            lines2 = f.readlines()

        # Unified diff
        diff = difflib.unified_diff(
            lines1,
            lines2,
            fromfile=f"{snapshot1_name}/{file_path}",
            tofile=f"{snapshot2_name}/{file_path}",
            lineterm=''
        )

        return '\n'.join(diff)

    def cleanup_old_snapshots(self, keep_last: int = 10, keep_manual: bool = True):
        """
        Wyczyść stare snapshoty

        Args:
            keep_last: Ile ostatnich snapshotów zachować
            keep_manual: Czy zachować wszystkie manualne snapshoty
        """
        snapshots = self.metadata["snapshots"]

        # Sortuj po dacie
        snapshots.sort(key=lambda x: x["timestamp"], reverse=True)

        to_delete = []
        auto_count = 0

        for snapshot in snapshots:
            if snapshot.get("auto", False):
                auto_count += 1
                if auto_count > keep_last:
                    to_delete.append(snapshot["name"])
            elif not keep_manual:
                # Usuń również stare manualne jeśli keep_manual=False
                if len(snapshots) - len(to_delete) > keep_last:
                    to_delete.append(snapshot["name"])

        # Usuń
        for snapshot_name in to_delete:
            self.delete_snapshot(snapshot_name)

    def _calculate_dir_hash(self, path: Path) -> str:
        """Oblicz hash MD5 całego folderu"""
        hash_md5 = hashlib.md5()

        for file_path in sorted(self._get_all_files(path)):
            full_path = path / file_path
            if full_path.is_file():
                hash_md5.update(str(file_path).encode())
                hash_md5.update(self._calculate_file_hash(full_path).encode())

        return hash_md5.hexdigest()

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Oblicz hash MD5 pojedynczego pliku"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _get_all_files(self, path: Path) -> List[str]:
        """Pobierz listę wszystkich plików w folderze (relatywne ścieżki)"""
        files = []
        for item in path.rglob("*"):
            if item.is_file():
                files.append(str(item.relative_to(path)))
        return files

    def _get_dir_size(self, path: Path) -> int:
        """Oblicz rozmiar folderu w bajtach"""
        total = 0
        for item in path.rglob("*"):
            if item.is_file():
                total += item.stat().st_size
        return total

    def get_snapshot_info(self, snapshot_name: str) -> Optional[Dict]:
        """Pobierz informacje o snapshocie"""
        return next(
            (s for s in self.metadata["snapshots"] if s["name"] == snapshot_name),
            None
        )

    def export_snapshot_metadata(self, output_path: Path):
        """Eksportuj metadata do pliku JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)


# ===== PRZYKŁAD UŻYCIA =====
if __name__ == "__main__":
    # Inicjalizacja
    sm = SnapshotManager()

    # Stwórz snapshot
    source = Path("./test_folder")
    snapshot = sm.create_snapshot(
        source,
        name="manual_backup_v1",
        description="Backup przed dużą zmianą",
        tags=["important", "pre-release"]
    )
    print(f"✅ Stworzono snapshot: {snapshot['name']}")

    # Lista snapshotów
    snapshots = sm.list_snapshots()
    print(f"\n📋 Snapshoty ({len(snapshots)}):")
    for s in snapshots:
        print(f"  - {s['name']} | {s['timestamp']} | {s['size_mb']:.2f} MB")

    # Porównaj snapshoty (jeśli masz 2+)
    if len(snapshots) >= 2:
        diff = sm.compare_snapshots(snapshots[0]['name'], snapshots[1]['name'])
        print(f"\n🔍 Różnice:")
        print(f"  Dodane: {len(diff['added'])}")
        print(f"  Usunięte: {len(diff['removed'])}")
        print(f"  Zmodyfikowane: {len(diff['modified'])}")

