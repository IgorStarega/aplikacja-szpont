#!/usr/bin/env python3
"""
QUICKSTART - Aktualizator Strony v5.0
Szybki start aplikacji
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 70)
    print("🔄 AKTUALIZATOR STRONY v5.0 - QUICKSTART")
    print("=" * 70)
    print()

    # Check Python
    print("📌 Python:", sys.version.split()[0])
    print()

    # Install dependencies
    print("📦 Instalowanie zależności...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
    print("✅ Zależności zainstalowane")
    print()

    # Create folders
    print("📁 Tworzenie folderów...")
    Path("src/.cache").mkdir(exist_ok=True)
    Path("src/.data/reports").mkdir(parents=True, exist_ok=True)
    Path("src/.config").mkdir(exist_ok=True)
    print("✅ Foldery stworzone")
    print()

    # Launch app
    print("🚀 Uruchamianie aplikacji v5.0...")
    print("-" * 70)
    subprocess.run([sys.executable, "apk.py"])

if __name__ == "__main__":
    main()

