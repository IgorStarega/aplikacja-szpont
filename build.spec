# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File dla Aktualizator Strony v5.3.0
Build standalone .exe bez Python'a - PRODUCTION READY

Użycie:
    pyinstaller build.spec

Output:
    dist/AktualizatorStrony.exe
"""

import os
from pathlib import Path

block_cipher = None

a = Analysis(
    ['apk.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('requirements.txt', '.'),
        ('TODO.md', '.'),
        ('img/ikona.png', 'img'),  # Dodaj ikonę PNG
        ('img/ikona.ico', 'img'),  # Dodaj ikonę ICO
    ],
    hiddenimports=[
        # GUI
        'customtkinter',
        'tkinter',
        'PIL',
        'PIL._tkinter_finder',
        # Core
        'beautifulsoup4',
        'bs4',
        'python-dotenv',
        'dotenv',
        'darkdetect',
        # Reports
        'openpyxl',
        'reportlab',
        # Scheduler & Notifications
        'schedule',
        'requests',
        'PyGithub',
        'github',
        'slack_sdk',
        'discord',
        # Web
        'flask',
        'flask_cors',
        'flask_socketio',
        # Database
        'sqlalchemy',
        'alembic',
        # Security
        'cryptography',
        'paramiko',
        'GitPython',
        'git',
        # v5.3.0 - Visualization
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.backends.backend_tkagg',
        'plotly',
        'plotly.graph_objs',
        'plotly.express',
        'kaleido',
        'numpy',
        'pandas',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'scipy',
        'pytest',
        'black',
        'pylint',
        'test',
        'tests',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AktualizatorStrony',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/ikona.ico' if os.path.exists('img/ikona.ico') else None,
)

