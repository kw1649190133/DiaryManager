# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

block_cipher = None

# 项目根目录（硬编码，PyInstaller 6.x 不提供 __file__）
ROOT = Path(r"C:\work\日记本应用开发\Diary_manager")

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # 图标文件（打包到 exe 同目录）
        (str(ROOT / "diary.ico"), "."),
    ],
    hiddenimports=[
        # PySide6 核心
        "shiboken6",
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        # 业务模块
        "core",
        "core.models",
        "core.storage",
        "core.diary_manager",
        "core.calendar_service",
        "cli",
        "cli.cli",
        "gui",
        "gui.main",
        "gui.main_window",
        "gui.calendar_view",
        "gui.diary_editor",
        "gui.stats_dialog",
        "gui.styles",
        "utils",
        "utils.date_utils",
    ],
    hookspath=[],
    hooksconfig={},
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,   # 不把二进制打包进 exe
    name="DiaryManager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,            # GUI 程序，无控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ROOT / "diary.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="DiaryManager",
)
