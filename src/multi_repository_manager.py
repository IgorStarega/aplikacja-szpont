"""
Multi Repository Manager dla Aktualizatora Strony v5.3.0
Zarządzanie wieloma repozytoriami jednocześnie

Funkcje:
- Zarządzanie wieloma repozytoriami
- Bulk operations (aktualizuj wszystkie)
- Repository profiles (dev/staging/prod)
- Dependency graph
- Synchronized updates
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class RepoProfile(Enum):
    """Profile repozytoriów"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    BACKUP = "backup"


@dataclass
class Repository:
    """Reprezentacja repozytorium"""
    name: str
    local_path: str
    remote_url: str
    branch: str
    profile: str
    enabled: bool = True
    auto_update: bool = False
    priority: int = 0  # Kolejność aktualizacji
    depends_on: List[str] = None  # Zależności od innych repo
    last_update: str = None
    description: str = ""

    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []


class MultiRepositoryManager:
    """Zarządzanie wieloma repozytoriami"""

    def __init__(self, config_path: Path = None):
        """
        Inicjalizacja Multi Repository Manager

        Args:
            config_path: Ścieżka do pliku konfiguracji
        """
        self.config_path = config_path or Path.cwd() / "config" / "repositories.json"
        self.repositories: Dict[str, Repository] = {}
        self._load_config()

    def _load_config(self):
        """Wczytaj konfigurację repozytoriów"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, repo_data in data.get("repositories", {}).items():
                        self.repositories[name] = Repository(**repo_data)
            except Exception as e:
                print(f"⚠️  Błąd wczytywania konfiguracji: {e}")
                self.repositories = {}
        else:
            self._create_default_config()

    def _save_config(self):
        """Zapisz konfigurację do pliku"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "repositories": {
                name: asdict(repo) for name, repo in self.repositories.items()
            }
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _create_default_config(self):
        """Stwórz domyślną konfigurację"""
        default_repos = {
            "main-website": Repository(
                name="main-website",
                local_path="./repos/main",
                remote_url="https://github.com/user/main-website.git",
                branch="main",
                profile=RepoProfile.PRODUCTION.value,
                priority=1,
                description="Główna strona produkcyjna"
            ),
            "staging-website": Repository(
                name="staging-website",
                local_path="./repos/staging",
                remote_url="https://github.com/user/staging-website.git",
                branch="develop",
                profile=RepoProfile.STAGING.value,
                priority=2,
                description="Środowisko testowe"
            ),
        }
        self.repositories = default_repos
        self._save_config()

    def add_repository(
        self,
        name: str,
        local_path: str,
        remote_url: str,
        branch: str = "main",
        profile: str = "development",
        **kwargs
    ) -> Repository:
        """
        Dodaj nowe repozytorium

        Args:
            name: Nazwa repozytorium
            local_path: Ścieżka lokalna
            remote_url: URL repozytorium
            branch: Gałąź
            profile: Profil (development/staging/production)
            **kwargs: Dodatkowe parametry

        Returns:
            Obiekt Repository
        """
        if name in self.repositories:
            raise ValueError(f"Repozytorium '{name}' już istnieje")

        repo = Repository(
            name=name,
            local_path=local_path,
            remote_url=remote_url,
            branch=branch,
            profile=profile,
            **kwargs
        )

        self.repositories[name] = repo
        self._save_config()
        return repo

    def remove_repository(self, name: str) -> bool:
        """Usuń repozytorium"""
        if name in self.repositories:
            del self.repositories[name]
            self._save_config()
            return True
        return False

    def update_repository(self, name: str, **kwargs) -> Optional[Repository]:
        """
        Zaktualizuj dane repozytorium

        Args:
            name: Nazwa repozytorium
            **kwargs: Pola do aktualizacji

        Returns:
            Zaktualizowany Repository lub None
        """
        if name not in self.repositories:
            return None

        repo = self.repositories[name]
        for key, value in kwargs.items():
            if hasattr(repo, key):
                setattr(repo, key, value)

        self._save_config()
        return repo

    def get_repository(self, name: str) -> Optional[Repository]:
        """Pobierz repozytorium po nazwie"""
        return self.repositories.get(name)

    def list_repositories(
        self,
        profile: str = None,
        enabled_only: bool = False
    ) -> List[Repository]:
        """
        Lista repozytoriów z opcjonalnym filtrowaniem

        Args:
            profile: Filtruj po profilu
            enabled_only: Tylko włączone

        Returns:
            Lista repozytoriów
        """
        repos = list(self.repositories.values())

        if profile:
            repos = [r for r in repos if r.profile == profile]

        if enabled_only:
            repos = [r for r in repos if r.enabled]

        # Sortuj po priorytecie
        repos.sort(key=lambda x: x.priority)

        return repos

    def get_update_order(self) -> List[Repository]:
        """
        Pobierz kolejność aktualizacji z uwzględnieniem zależności

        Returns:
            Lista repozytoriów w kolejności aktualizacji
        """
        repos = [r for r in self.repositories.values() if r.enabled]

        # Topological sort dla zależności
        visited = set()
        temp_visited = set()
        order = []

        def visit(repo: Repository):
            if repo.name in temp_visited:
                raise ValueError(f"Cykliczna zależność wykryta dla: {repo.name}")

            if repo.name in visited:
                return

            temp_visited.add(repo.name)

            # Odwiedź zależności
            for dep_name in repo.depends_on:
                if dep_name in self.repositories:
                    dep_repo = self.repositories[dep_name]
                    if dep_repo.enabled:
                        visit(dep_repo)

            temp_visited.remove(repo.name)
            visited.add(repo.name)
            order.append(repo)

        # Odwiedź wszystkie repo
        for repo in sorted(repos, key=lambda x: x.priority):
            if repo.name not in visited:
                visit(repo)

        return order

    def bulk_update_status(self, status: bool, profile: str = None):
        """
        Włącz/wyłącz wiele repozytoriów

        Args:
            status: True = włącz, False = wyłącz
            profile: Opcjonalnie tylko dla profilu
        """
        for repo in self.repositories.values():
            if profile is None or repo.profile == profile:
                repo.enabled = status

        self._save_config()

    def get_statistics(self) -> Dict:
        """Pobierz statystyki repozytoriów"""
        repos = list(self.repositories.values())

        stats = {
            "total": len(repos),
            "enabled": sum(1 for r in repos if r.enabled),
            "disabled": sum(1 for r in repos if not r.enabled),
            "auto_update": sum(1 for r in repos if r.auto_update),
            "by_profile": {}
        }

        # Statystyki per profil
        for profile in RepoProfile:
            count = sum(1 for r in repos if r.profile == profile.value)
            stats["by_profile"][profile.value] = count

        return stats

    def export_config(self, output_path: Path):
        """Eksportuj konfigurację do pliku"""
        with open(output_path, 'w', encoding='utf-8') as f:
            data = {
                "repositories": {
                    name: asdict(repo) for name, repo in self.repositories.items()
                }
            }
            json.dump(data, f, indent=2, ensure_ascii=False)

    def import_config(self, input_path: Path, merge: bool = False):
        """
        Importuj konfigurację z pliku

        Args:
            input_path: Ścieżka do pliku
            merge: Czy scalić z istniejącymi (True) czy nadpisać (False)
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if not merge:
                self.repositories = {}

            for name, repo_data in data.get("repositories", {}).items():
                self.repositories[name] = Repository(**repo_data)

        self._save_config()

    def validate_dependencies(self) -> Dict[str, List[str]]:
        """
        Sprawdź poprawność zależności

        Returns:
            Dict z błędami (nazwa repo -> lista błędów)
        """
        errors = {}

        for name, repo in self.repositories.items():
            repo_errors = []

            for dep_name in repo.depends_on:
                if dep_name not in self.repositories:
                    repo_errors.append(f"Nieistniejąca zależność: {dep_name}")
                elif not self.repositories[dep_name].enabled:
                    repo_errors.append(f"Wyłączona zależność: {dep_name}")

            if repo_errors:
                errors[name] = repo_errors

        return errors

    def mark_updated(self, name: str):
        """Oznacz repozytorium jako zaktualizowane"""
        if name in self.repositories:
            self.repositories[name].last_update = datetime.now().isoformat()
            self._save_config()


# ===== PRZYKŁAD UŻYCIA =====
if __name__ == "__main__":
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
    print("📋 Repozytoria:")
    for repo in mrm.list_repositories():
        print(f"  - {repo.name} ({repo.profile}) | Priority: {repo.priority}")

    # Kolejność aktualizacji
    print("\n🔄 Kolejność aktualizacji:")
    update_order = mrm.get_update_order()
    for i, repo in enumerate(update_order, 1):
        print(f"  {i}. {repo.name}")

    # Statystyki
    stats = mrm.get_statistics()
    print(f"\n📊 Statystyki:")
    print(f"  Total: {stats['total']}")
    print(f"  Enabled: {stats['enabled']}")
    print(f"  Auto-update: {stats['auto_update']}")

    # Walidacja zależności
    errors = mrm.validate_dependencies()
    if errors:
        print(f"\n⚠️  Błędy zależności:")
        for repo_name, repo_errors in errors.items():
            print(f"  {repo_name}:")
            for error in repo_errors:
                print(f"    - {error}")
    else:
        print("\n✅ Wszystkie zależności poprawne")

