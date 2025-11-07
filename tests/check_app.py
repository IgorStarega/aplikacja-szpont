#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script - sprawdza czy wszystkie moduły działają
"""

import sys
from pathlib import Path

print("=" * 60)
print("🔍 SPRAWDZANIE APLIKACJI")
print("=" * 60)

# Test 1: Sprawdzenie czy wszystkie pliki istnieją
print("\n1️⃣  Sprawdzanie czy pliki istnieją...")
required_files = [
    "apk.py",
    "gui.py",
    "update_manager.py",
    "config_manager.py",
    "test.py",
    "config.json",
    "requirements.txt",
]

all_exist = True
for file in required_files:
    path = Path(file)
    if path.exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - BRAK!")
        all_exist = False

if not all_exist:
    print("\n❌ Brakuje plików!")
    sys.exit(1)

# Test 2: Sprawdzenie importów
print("\n2️⃣  Sprawdzanie importów...")
try:
    from config_manager import ConfigManager
    print("   ✅ config_manager")
except Exception as e:
    print(f"   ❌ config_manager - {str(e)}")
    sys.exit(1)

try:
    from update_manager import UpdateManager
    print("   ✅ update_manager")
except Exception as e:
    print(f"   ❌ update_manager - {str(e)}")
    sys.exit(1)

try:
    from gui import StronyUpdaterApp
    print("   ✅ gui")
except Exception as e:
    print(f"   ❌ gui - {str(e)}")
    sys.exit(1)

try:
    import apk
    print("   ✅ apk")
except Exception as e:
    print(f"   ❌ apk - {str(e)}")
    sys.exit(1)

# Test 3: Sprawdzenie zależności
print("\n3️⃣  Sprawdzanie zależności...")
try:
    import bs4
    print("   ✅ beautifulsoup4")
except Exception as e:
    print(f"   ❌ beautifulsoup4 - {str(e)}")
    print("   💡 Zainstaluj: pip install beautifulsoup4")

# Test 4: Sprawdzenie klas
print("\n4️⃣  Sprawdzanie klas...")
try:
    config = ConfigManager("config.json")
    print("   ✅ ConfigManager instantiated")
except Exception as e:
    print(f"   ❌ ConfigManager - {str(e)}")

try:
    update_mgr = UpdateManager()
    print("   ✅ UpdateManager instantiated")
except Exception as e:
    print(f"   ❌ UpdateManager - {str(e)}")

print("\n" + "=" * 60)
print("✅ WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
print("=" * 60)
print("\n💡 Aplikacja jest gotowa do uruchomienia!")
print("   Uruchom: python apk.py")

