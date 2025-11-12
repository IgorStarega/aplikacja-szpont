#!/usr/bin/env python3
"""
Release Package Script - v5.1
Pakuje aplikację do dystrybucji
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_release_package():
    """Stwórz paczkę release'u"""

    print("📦 TWORZENIE PACZKI RELEASE - v5.1")
    print("=" * 70)

    app_dir = Path(__file__).parent
    release_dir = app_dir / "release"
    release_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    release_name = f"AktualizatorStrony-v5.1-{timestamp}"
    release_path = release_dir / release_name
    release_path.mkdir(exist_ok=True)

    print(f"\n📁 Katalog release: {release_path}")

    # Kopiuj pliki główne
    print("\n📋 Kopiowanie plików...")
    files_to_copy = [
        "apk.py",
        "README.md",
        "TODO.md",
        "requirements.txt",
        "config.json",
        ".env.example",
        "QUICKSTART.py"
    ]

    for file in files_to_copy:
        src = app_dir / file
        if src.exists():
            shutil.copy2(src, release_path / file)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} - nie znaleziono")

    # Kopiuj folder src
    print("\n📁 Kopiowanie src/...")
    src_src = app_dir / "src"
    dst_src = release_path / "src"

    if src_src.exists():
        shutil.copytree(src_src, dst_src,
                       ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        print(f"  ✅ src/ skopiowany")

    # Kopiuj docs
    print("\n📁 Kopiowanie docs/...")
    src_docs = app_dir / "docs"
    dst_docs = release_path / "docs"

    if src_docs.exists():
        shutil.copytree(src_docs, dst_docs,
                       ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        print(f"  ✅ docs/ skopiowany")

    # Stwórz README dla release'u
    readme_content = """# 🔄 Aktualizator Strony v5.1 - Release Package

## 📋 Co zawiera

- ✅ Pełna aplikacja v5.1
- ✅ Wszystkie moduły (13)
- ✅ Konfiguracja
- ✅ Dokumentacja
- ✅ Przykłady

## 🚀 Szybki Start

### 1. Instalacja

```bash
pip install -r requirements.txt
```

### 2. Konfiguracja

```bash
cp .env.example .env
# Edytuj .env i ustaw ścieżki repozytoriów
```

### 3. Uruchomienie

```bash
python apk.py
```

## 📊 Wersja Informacje

- **Wersja**: 5.1
- **Status**: PRODUCTION READY
- **Data**: """ + datetime.now().strftime("%Y-%m-%d") + """
- **Features**: 23+
- **Moduły**: 13

## 📁 Struktura

```
├── apk.py              - Główna aplikacja
├── src/                - Kod źródłowy (13 modułów)
├── docs/               - Dokumentacja
├── README.md           - Dokumentacja główna
├── TODO.md             - Mapa drogowa
└── requirements.txt    - Zależności Python
```

## 🔐 Security

- AES-256 Encryption
- SSH Key Management
- Git Credentials Storage
- GitHub Webhook Verification

## 🌐 Integration

- Web Dashboard (Flask)
- REST API (18+ endpoints)
- GitHub Webhooks
- Slack, Discord, Email

## 📞 Wsparcie

Czytaj dokumentację:
- docs/INSTRUKCJA.md - Instrukcja obsługi
- docs/TROUBLESHOOTING.md - Rozwiązywanie problemów
- docs/API_REFERENCE.md - Referencja API

---

**Status**: ✅ PRODUCTION READY  
**Data**: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
"""

    readme_path = release_path / "RELEASE_README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  ✅ RELEASE_README.md stworzony")

    # Stwórz manifest
    print("\n📝 Tworzenie manifestu...")
    manifest = {
        "version": "5.1",
        "date": datetime.now().isoformat(),
        "status": "PRODUCTION READY",
        "modules": 13,
        "features": 23,
        "files": len(list(release_path.rglob("*"))),
        "security": "AES-256 + SSH",
        "api_endpoints": 18
    }

    import json
    manifest_path = release_path / "MANIFEST.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"  ✅ MANIFEST.json stworzony")

    # Stwórz ZIP
    print(f"\n📦 Kompresja do ZIP...")
    zip_path = release_dir / f"{release_name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in release_path.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(release_dir)
                zipf.write(file, arcname)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"  ✅ {release_name}.zip ({size_mb:.1f} MB)")

    # Podsumowanie
    print("\n" + "=" * 70)
    print("✅ RELEASE PACKAGE GOTOWY!")
    print("=" * 70)
    print(f"\n📁 Lokalizacja: {zip_path}")
    print(f"   Rozmiar: {size_mb:.1f} MB")
    print(f"\n📋 Zawartość:")
    print(f"   - Plik ZIP: {release_name}.zip")
    print(f"   - Folder: {release_path.name}")
    print(f"\n🚀 Dystrybucja gotowa!")
    print(f"   Prześlij: {zip_path}")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(create_release_package())

