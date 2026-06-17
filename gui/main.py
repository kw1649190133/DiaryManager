"""GUI 入口文件"""

import sys
import os
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow


def _get_icon_path() -> Path | None:
    """获取程序图标路径，兼容源码运行和 PyInstaller 打包"""
    if getattr(sys, "frozen", False):
        # PyInstaller 打包模式：exe 同目录下找
        base = Path(sys.executable).parent
        p = base / "diary.ico"
        if p.exists():
            return p
        # onedir 模式下也可能在 _internal/
        p2 = base / "_internal" / "diary.ico"
        if p2.exists():
            return p2
    else:
        # 源码模式：项目根目录
        p = Path(__file__).parent.parent / "diary.ico"
        if p.exists():
            return p
    return None


def main(data_dir: str = "data"):
    """启动 GUI

    Args:
        data_dir: 数据存储目录
    """
    # 确保数据目录存在
    Path(data_dir).mkdir(parents=True, exist_ok=True)

    app = QApplication(sys.argv)

    # 设置应用信息
    app.setApplicationName("我的日记本")
    app.setOrganizationName("DiaryApp")

    # 设置程序图标
    icon_path = _get_icon_path()
    if icon_path:
        icon = QIcon(str(icon_path))
        app.setWindowIcon(icon)
    else:
        print(f"Warning: diary.ico not found")

    # 创建主窗口
    window = MainWindow(data_dir=data_dir)
    window.setWindowIcon(icon if icon_path else QIcon())
    window.show()

    return app.exec()
