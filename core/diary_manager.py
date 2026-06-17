"""日记管理器 - 核心业务逻辑"""

from datetime import date
from pathlib import Path
from typing import Iterator, Optional

from .models import DiaryEntry, DiaryStats, MonthStats
from .storage import FileDiaryStorage


class DiaryManager:
    """日记管理器

    负责日记的增删改查业务逻辑，不涉及 UI。
    支持依赖注入，可替换存储实现。
    """

    def __init__(self, storage: Optional[FileDiaryStorage] = None):
        """初始化日记管理器

        Args:
            storage: 存储实例，默认使用 FileDiaryStorage
        """
        self.storage = storage or FileDiaryStorage()

    # ==================== CRUD 操作 ====================

    def create(self, diary_date: date, content: str = "") -> DiaryEntry:
        """创建新日记（仅当日期不存在时）

        Args:
            diary_date: 日期
            content: 初始内容

        Returns:
            创建的日记条目

        Raises:
            FileExistsError: 如果日记已存在
        """
        if self.exists(diary_date):
            raise FileExistsError(f"日记 {diary_date} 已存在")

        entry = DiaryEntry(date=diary_date, content=content)
        self.storage.save(entry)
        return entry

    def save(self, diary_date: date, content: str) -> DiaryEntry:
        """保存日记（存在则覆盖，不存在则创建）

        Args:
            diary_date: 日期
            content: 日记内容

        Returns:
            保存的日记条目
        """
        entry = DiaryEntry(date=diary_date, content=content)
        self.storage.save(entry)
        return entry

    def load(self, diary_date: date) -> Optional[DiaryEntry]:
        """加载指定日期的日记

        Args:
            diary_date: 日期

        Returns:
            日记条目，不存在则返回 None
        """
        return self.storage.load(diary_date)

    def delete(self, diary_date: date) -> bool:
        """删除指定日期的日记

        Args:
            diary_date: 日期

        Returns:
            是否成功删除
        """
        return self.storage.delete(diary_date)

    def exists(self, diary_date: date) -> bool:
        """检查日记是否存在

        Args:
            diary_date: 日期

        Returns:
            是否存在
        """
        return self.storage.exists(diary_date)

    # ==================== 列表查询 ====================

    def list_all(self) -> Iterator[DiaryEntry]:
        """列出所有日记（按日期降序）"""
        entries = list(self.storage.list_all_entries())
        return reversed(entries) if entries else iter([])

    def list_by_year(self, year: int) -> Iterator[DiaryEntry]:
        """列出指定年份的日记"""
        return self.storage.list_entries_by_year(year)

    def list_by_month(self, year: int, month: int) -> Iterator[DiaryEntry]:
        """列出指定月份的日记"""
        return self.storage.list_entries_by_month(year, month)

    def get_all_years(self) -> list[int]:
        """获取所有有日记的年份"""
        return self.storage.get_all_years()

    # ==================== 搜索功能 ====================

    def search(self, keyword: str, case_sensitive: bool = False) -> list[DiaryEntry]:
        """搜索日记内容

        Args:
            keyword: 搜索关键词
            case_sensitive: 是否区分大小写

        Returns:
            匹配的日记列表
        """
        results = []
        search_keyword = keyword if case_sensitive else keyword.lower()

        for entry in self.storage.list_all_entries():
            content = entry.content if case_sensitive else entry.content.lower()
            if search_keyword in content:
                results.append(entry)

        return results

    def search_by_title(self, keyword: str, case_sensitive: bool = False) -> list[DiaryEntry]:
        """按标题搜索（取每行的第一个字符/词作为标题）"""
        results = []
        search_keyword = keyword if case_sensitive else keyword.lower()

        for entry in self.storage.list_all_entries():
            first_line = entry.content.split('\n')[0] if entry.content else ""
            search_line = first_line if case_sensitive else first_line.lower()
            if search_keyword in search_line:
                results.append(entry)

        return results

    # ==================== 统计功能 ====================

    def get_stats(self) -> DiaryStats:
        """获取全局统计信息

        Returns:
            统计信息
        """
        entries = list(self.storage.list_all_entries())

        if not entries:
            return DiaryStats()

        total_days = len(entries)
        total_words = sum(e.word_count for e in entries)
        avg_words = total_words / total_days if total_days > 0 else 0

        # 找出最长和最短的日记
        sorted_by_words = sorted(entries, key=lambda e: e.word_count)

        return DiaryStats(
            total_days=total_days,
            total_words=total_words,
            avg_words_per_day=round(avg_words, 1),
            longest_day=sorted_by_words[-1].date if sorted_by_words else None,
            longest_words=sorted_by_words[-1].word_count if sorted_by_words else 0,
            shortest_day=sorted_by_words[0].date if sorted_by_words else None,
            shortest_words=sorted_by_words[0].word_count if sorted_by_words else 0,
            entries=entries
        )

    def get_year_stats(self, year: int) -> DiaryStats:
        """获取指定年份的统计信息

        Args:
            year: 年份

        Returns:
            统计信息
        """
        entries = list(self.storage.list_entries_by_year(year))

        if not entries:
            return DiaryStats()

        total_days = len(entries)
        total_words = sum(e.word_count for e in entries)
        avg_words = total_words / total_days if total_days > 0 else 0

        sorted_by_words = sorted(entries, key=lambda e: e.word_count)

        return DiaryStats(
            total_days=total_days,
            total_words=total_words,
            avg_words_per_day=round(avg_words, 1),
            longest_day=sorted_by_words[-1].date if sorted_by_words else None,
            longest_words=sorted_by_words[-1].word_count if sorted_by_words else 0,
            shortest_day=sorted_by_words[0].date if sorted_by_words else None,
            shortest_words=sorted_by_words[0].word_count if sorted_by_words else 0,
            entries=entries
        )

    def get_month_stats(self, year: int, month: int) -> MonthStats:
        """获取指定月份的统计信息

        Args:
            year: 年份
            month: 月份

        Returns:
            月度统计
        """
        entries = list(self.storage.list_entries_by_month(year, month))
        dates = [e.date for e in entries]

        return MonthStats(
            year=year,
            month=month,
            total_days=len(entries),
            total_words=sum(e.word_count for e in entries),
            dates_with_entries=sorted(dates)
        )

    def get_day_word_count(self, diary_date: date) -> int:
        """获取指定日期的字数

        Args:
            diary_date: 日期

        Returns:
            字数
        """
        entry = self.load(diary_date)
        return entry.word_count if entry else 0

    # ==================== 导入功能 ====================

    def import_directory(self, source_dir: Path, recursive: bool = True) -> dict:
        """从目录导入日记文件

        自动识别符合 YYYYMMDD.txt 或 YYYYMMDD.md 格式的文件。

        Args:
            source_dir: 源目录
            recursive: 是否递归子目录

        Returns:
            导入结果统计
        """
        imported = 0
        skipped = 0
        messages = []

        extensions = (".txt", ".md")

        def get_files():
            if recursive:
                for ext in extensions:
                    yield from source_dir.rglob(f"*{ext}")
            else:
                for file in source_dir.iterdir():
                    if file.is_file() and file.suffix in extensions:
                        yield file

        for file_path in get_files():
            success, msg = self.storage.import_file(file_path)
            messages.append(msg)
            if success:
                imported += 1
            else:
                skipped += 1

        return {
            "imported": imported,
            "skipped": skipped,
            "messages": messages
        }

    def auto_import(self) -> dict:
        """自动导入 data 目录下尚未管理的日记文件

        扫描 base_dir 下的所有 .txt 和 .md 文件，
        如果文件不在正确的年份子目录下，则导入。

        Returns:
            导入结果统计
        """
        imported = 0
        skipped = 0
        messages = []

        # 扫描 data 根目录和所有年份目录
        scan_dirs = [self.storage.base_dir]
        scan_dirs.extend(d for d in self.storage.base_dir.iterdir() if d.is_dir())

        for scan_dir in scan_dirs:
            for file_path in scan_dir.iterdir():
                if not file_path.is_file():
                    continue

                if file_path.suffix not in (".txt", ".md"):
                    continue

                name = file_path.stem
                if len(name) != 8 or not name.isdigit():
                    continue

                # 检查是否已经在正确的位置
                try:
                    from datetime import datetime
                    diary_date = datetime.strptime(name, "%Y%m%d").date()
                    correct_path = self.storage.get_file_path(diary_date)

                    if file_path.resolve() == correct_path.resolve():
                        # 已经在正确位置，跳过
                        skipped += 1
                        continue

                    # 不在正确位置，导入
                    success, msg = self.storage.import_file(file_path)
                    messages.append(msg)
                    if success:
                        imported += 1
                    else:
                        skipped += 1
                except ValueError:
                    skipped += 1
                    messages.append(f"跳过（无效日期）: {file_path.name}")

        return {
            "imported": imported,
            "skipped": skipped,
            "messages": messages
        }
