"""命令行接口主模块"""

import argparse
import shlex
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from core import DiaryManager, CalendarService
from utils.date_utils import parse_date_str


class CLI:
    """日记命令行接口"""

    def __init__(self, data_dir: str = "data"):
        """初始化 CLI

        Args:
            data_dir: 数据存储目录
        """
        self.manager = DiaryManager()
        self.calendar = CalendarService(self.manager.storage)
        self.data_dir = Path(data_dir).resolve()

    # ==================== 命令处理 ====================

    def cmd_new(self, date_str: str, content: str = "") -> bool:
        """新建日记"""
        try:
            diary_date = parse_date_str(date_str)
            entry = self.manager.create(diary_date, content)
            print(f"✅ 已创建日记: {entry}")
            return True
        except FileExistsError as e:
            print(f"⚠️  {e}")
            return False
        except ValueError as e:
            print(f"❌ 日期格式错误: {e}")
            return False

    def cmd_save(self, date_str: str, content: str) -> bool:
        """保存日记"""
        try:
            diary_date = parse_date_str(date_str)
            entry = self.manager.save(diary_date, content)
            print(f"✅ 已保存: {entry}")
            return True
        except ValueError as e:
            print(f"❌ 日期格式错误: {e}")
            return False

    def cmd_view(self, date_str: str) -> bool:
        """查看日记"""
        try:
            diary_date = parse_date_str(date_str)
            entry = self.manager.load(diary_date)
            if entry:
                print(entry.content)
            else:
                print(f"⚠️  日记 {diary_date} 不存在")
            return True
        except ValueError as e:
            print(f"❌ 日期格式错误: {e}")
            return False

    def cmd_delete(self, date_str: str) -> bool:
        """删除日记"""
        try:
            diary_date = parse_date_str(date_str)
            if self.manager.delete(diary_date):
                print(f"🗑️  已删除日记: {diary_date}")
                return True
            else:
                print(f"⚠️  日记 {diary_date} 不存在")
                return False
        except ValueError as e:
            print(f"❌ 日期格式错误: {e}")
            return False

    def cmd_list(self, year_or_all: Optional[str] = None, month: Optional[int] = None) -> bool:
        """列出日记"""
        if year_or_all is None:
            # 列出最近
            recent = self.calendar.get_recent_diary_dates(10)
            if not recent:
                print("📭 暂无日记")
                return True
            print("📝 最近的日记:")
            for d in recent:
                entry = self.manager.load(d)
                status = f"({entry.word_count}字)" if entry else ""
                print(f"  {d.strftime('%Y-%m-%d')} {status}")
            return True

        if year_or_all.lower() == "all":
            # 列出所有日记
            years = self.manager.get_all_years()
            if not years:
                print("📭 暂无日记")
                return True

            for year in years:
                entries = list(self.manager.list_by_year(year))
                print(f"\n📅 {year}年 ({len(entries)}篇)")
                for entry in entries:
                    print(f"  {entry.date.strftime('%Y-%m-%d')} - {entry.word_count}字")
            return True

        try:
            year = int(year_or_all)
            entries = list(self.manager.list_by_year(year))

            if not entries:
                print(f"📭 {year}年暂无日记")
                return True

            if month:
                entries = [e for e in entries if e.month == month]
                if not entries:
                    print(f"📭 {year}年{month}月暂无日记")
                    return True
                print(f"\n📅 {year}年{month}月 ({len(entries)}篇)")
            else:
                print(f"\n📅 {year}年 ({len(entries)}篇)")

            for entry in entries:
                print(f"  {entry.date.strftime('%Y-%m-%d')} - {entry.word_count}字")
            return True

        except ValueError:
            print(f"❌ 无效的年份: {year_or_all}")
            return False

    def cmd_search(self, keyword: str, case_sensitive: bool = False) -> bool:
        """搜索日记"""
        results = self.manager.search(keyword, case_sensitive)

        if not results:
            print(f"🔍 没有找到包含 '{keyword}' 的日记")
            return True

        print(f"🔍 找到 {len(results)} 篇日记:")
        for entry in results:
            # 显示匹配行的上下文
            content = entry.content
            idx = content.lower().find(keyword.lower() if not case_sensitive else keyword)
            start = max(0, idx - 30)
            end = min(len(content), idx + len(keyword) + 30)
            snippet = content[start:end].replace('\n', ' ')

            if start > 0:
                snippet = '...' + snippet
            if end < len(content):
                snippet = snippet + '...'

            print(f"\n📄 {entry.date.strftime('%Y-%m-%d')} ({entry.word_count}字)")
            print(f"   {snippet}")

        return True

    def cmd_stats(self, year: Optional[int] = None) -> bool:
        """显示统计信息"""
        if year:
            stats = self.manager.get_year_stats(year)
            print(f"\n📊 {year}年统计:")
        else:
            stats = self.manager.get_stats()
            print(f"\n📊 全局统计:")

        print(f"  写了日记: {stats.total_days} 天")
        print(f"  总字数: {stats.total_words} 字")
        print(f"  平均每天: {stats.avg_words_per_day} 字")

        if stats.longest_day:
            print(f"  最多一天: {stats.longest_day} ({stats.longest_words}字)")
        if stats.shortest_day:
            print(f"  最少一天: {stats.shortest_day} ({stats.shortest_words}字)")

        return True

    def cmd_calendar(self, year: Optional[int] = None, month: Optional[int] = None) -> bool:
        """显示日历"""
        today = date.today()
        year = year or today.year
        month = month or today.month

        data = self.calendar.get_month_calendar_data(year, month)

        month_names = ["", "一月", "二月", "三月", "四月", "五月", "六月",
                       "七月", "八月", "九月", "十月", "十一月", "十二月"]
        weekday_names = ["一", "二", "三", "四", "五", "六", "日"]

        print(f"\n      {year}年 {month_names[month]}")
        print(f"  {'  '.join(weekday_names)}")

        for week in data["weeks"]:
            line = []
            for day in week:
                if day is None:
                    line.append("   ")
                else:
                    d = day["day"]
                    marker = "●" if day["has_diary"] else "○"
                    line.append(f"{marker}{d:2d}")
            print("  " + "  ".join(line))

        print(f"\n  ● = 有日记  ○ = 无日记")
        if data["missing_dates"]:
            print(f"  本月未写日记: {len(data['missing_dates'])} 天")

        return True

    def cmd_import(self, source_dir: str, recursive: bool = True) -> bool:
        """导入目录"""
        source = Path(source_dir).resolve()
        if not source.exists():
            print(f"❌ 目录不存在: {source}")
            return False

        result = self.manager.import_directory(source, recursive)
        print(f"\n📥 导入完成:")
        print(f"  成功: {result['imported']}")
        print(f"  跳过: {result['skipped']}")

        return True

    def cmd_auto_import(self) -> bool:
        """自动导入"""
        result = self.manager.auto_import()
        print(f"\n🔄 自动导入完成:")
        print(f"  导入: {result['imported']}")
        print(f"  跳过: {result['skipped']}")

        if result["imported"] > 0:
            print("\n💡 使用 'diary list all' 查看导入的日记")

        return True

    # ==================== 解析器 ====================

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        """创建命令行参数解析器"""
        parser = argparse.ArgumentParser(
            prog="diary",
            description="📖 日记管理工具",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        subparsers = parser.add_subparsers(dest="command", help="可用命令")

        # new
        p_new = subparsers.add_parser("new", help="新建日记")
        p_new.add_argument("date", help="日期 (YYYY-MM-DD 或 YYYYMMDD)")
        p_new.add_argument("--content", "-c", default="", help="初始内容")

        # save
        p_save = subparsers.add_parser("save", help="保存日记（存在则覆盖）")
        p_save.add_argument("date", help="日期")
        p_save.add_argument("--content", "-c", required=True, help="日记内容")

        # view
        p_view = subparsers.add_parser("view", help="查看日记")
        p_view.add_argument("date", help="日期")

        # delete
        p_del = subparsers.add_parser("delete", help="删除日记")
        p_del.add_argument("date", help="日期")

        # list
        p_list = subparsers.add_parser("list", help="列出日记")
        p_list.add_argument("year_or_all", nargs="?", help="年份或 'all'")
        p_list.add_argument("--month", "-m", type=int, help="月份 (1-12)")

        # search
        p_search = subparsers.add_parser("search", help="搜索日记内容")
        p_search.add_argument("keyword", help="搜索关键词")
        p_search.add_argument("--case", "-C", action="store_true", help="区分大小写")

        # stats
        p_stats = subparsers.add_parser("stats", help="显示统计信息")
        p_stats.add_argument("year", nargs="?", type=int, help="年份")

        # calendar
        p_cal = subparsers.add_parser("calendar", help="显示日历")
        p_cal.add_argument("year", nargs="?", type=int, help="年份")
        p_cal.add_argument("month", nargs="?", type=int, help="月份")

        # import
        p_imp = subparsers.add_parser("import", help="从目录导入日记")
        p_imp.add_argument("source_dir", help="源目录")
        p_imp.add_argument("--no-recursive", action="store_true", help="不递归子目录")

        # auto-import
        subparsers.add_parser("auto-import", help="自动导入 data 目录下的日记文件")

        return parser

    # ==================== 运行 ====================

    def run_command(self, args: argparse.Namespace) -> bool:
        """执行命令"""
        if args.command is None:
            self.cmd_list()
            return True

        handlers = {
            "new": lambda: self.cmd_new(args.date, args.content),
            "save": lambda: self.cmd_save(args.date, args.content),
            "view": lambda: self.cmd_view(args.date),
            "delete": lambda: self.cmd_delete(args.date),
            "list": lambda: self.cmd_list(args.year_or_all, getattr(args, "month", None)),
            "search": lambda: self.cmd_search(args.keyword, getattr(args, "case", False)),
            "stats": lambda: self.cmd_stats(getattr(args, "year", None)),
            "calendar": lambda: self.cmd_calendar(
                getattr(args, "year", None),
                getattr(args, "month", None)
            ),
            "import": lambda: self.cmd_import(
                args.source_dir,
                not getattr(args, "no_recursive", False)
            ),
            "auto-import": lambda: self.cmd_auto_import(),
        }

        handler = handlers.get(args.command)
        if handler:
            return handler()

        print(f"❌ 未知命令: {args.command}")
        return False

    def run_interactive(self) -> None:
        """进入交互模式"""
        print("📖 日记管理程序（交互模式）")
        print("输入 'help' 查看命令，输入 'quit' 退出。\n")

        parser = self.create_parser()

        while True:
            try:
                user_input = input("diary> ").strip()
                if not user_input:
                    continue
                if user_input in ("quit", "exit", "q"):
                    print("👋 再见！")
                    break
                if user_input == "help":
                    parser.print_help()
                    continue

                # 解析命令
                try:
                    args = parser.parse_args(shlex.split(user_input))
                except SystemExit:
                    continue
                except ValueError as e:
                    print(f"⚠️  命令解析错误: {e}")
                    continue

                self.run_command(args)

            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except EOFError:
                print("\n👋 再见！")
                break

    def run(self, argv: list[str] | None = None) -> int:
        """运行 CLI

        Args:
            argv: 命令行参数（None 则从 sys.argv 读取）

        Returns:
            退出码（0 成功，1 失败）
        """
        parser = self.create_parser()
        args = parser.parse_args(argv)

        # 如果有命令参数，执行一次就退出
        if args.command is not None:
            success = self.run_command(args)
            return 0 if success else 1

        # 否则进入交互模式
        self.run_interactive()
        return 0
