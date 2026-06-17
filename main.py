"""日记本应用入口

支持两种运行模式:
1. 命令行模式: python main.py <command> [args]
2. 图形界面模式: python main.py --gui
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        prog="diary",
        description="📖 日记管理工具"
    )
    parser.add_argument("--gui", "-g", action="store_true", help="启动图形界面")
    parser.add_argument("--data-dir", "-d", default="data", help="数据存储目录")
    parser.add_argument("command", nargs="*", help="命令行参数")

    args = parser.parse_args()

    if args.gui or not args.command:
        # 启动 GUI
        try:
            from gui.main import main as gui_main
            gui_main(data_dir=args.data_dir)
        except ImportError as e:
            print(f"❌ 无法启动 GUI: {e}")
            print("\n请确保已安装 PySide6:")
            print("  pip install PySide6")
            sys.exit(1)
    else:
        # 启动 CLI
        from cli.cli import CLI
        cli = CLI(data_dir=args.data_dir)
        sys.exit(cli.run(args.command))


if __name__ == "__main__":
    main()
