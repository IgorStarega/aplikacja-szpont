"""
Aktualizator Strony - dziadu.dev
Główny punkt wejścia aplikacji

Wersja: 5.2 (PRODUCTION READY)
Status: ✅ GOTOWA DO UŻYTKU

Cechy v4.1:
- ⚡ Batch Processing (ThreadPoolExecutor, +3x szybciej!)
- 💾 Caching Struktury Folderów (MD5 hashing, -60% czasu)
- 🔄 Asynchroniczne Git Operacje (GUI zawsze responsywne)
- 📊 Inteligentne Różnicowanie (porównywanie HTML)
- 📈 Incremental Updates (tylko zmieniane foldery)
- ✨ Nowoczesne GUI (customtkinter)
- 🌙 Dark/Light Mode Toggle
- ⏱️ Progress Bar z ETA
- 🔐 Environment Variables (.env support)
- 📝 Logging Settings

Cechy v5.0:
- 📊 SQLite Historia Aktualizacji + Analytics
- 📈 Dashboard ze Statystykami
- 📄 Eksport Raportów (PDF/Excel)
- 💾 Backup Management UI
- 📅 Harmonogram Aktualizacji (Scheduler)
- 🔗 Webhook Integration (GitHub)
- 🔐 SSH Key Support
- 💬 Slack Integration
- 🎮 Discord Integration
- 📧 Email Reports

Cechy v5.1:
- 🌐 Web Dashboard (Flask)
- 🛠️  REST API
- 🔌 Webhook Manager
- 🔑 Credentials Manager

Cechy v5.2 (NOWE!):
- 🐳 Docker Support
- 📦 PyInstaller Build
- 🔄 Auto-Update Feature
- 📱 Mobile API
"""

import sys
from pathlib import Path

# Dodaj folder src/ do ścieżki Python
sys.path.insert(0, str(Path(__file__).parent / "src"))

import customtkinter as ctk
from gui_modern import ModernGUI

def main():
    """Uruchomienie aplikacji z nowoczesnym GUI v5.2"""
    root = ctk.CTk()
    app = ModernGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()



