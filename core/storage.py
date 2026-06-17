"""文件存储层 - 负责数据的持久化"""

import shutil
from datetime import date, datetime
from pathlib import Path
from typing import Iterator, Optional

from .models import DiaryEntry


class FileDiaryStorage:
    """基于文件系统的日记存储

    数据结构:
        data/
        ├── 2024/
        │   ├── 20240101.txt
        │   ├── 20240102.txt
        │   └── ...
        └── 2025/
            └── ...

    支持的文件格式: .txt, .md
    """

    def __init__(self, base_dir: str = "data"):
        """初始化存储

        Args:
            base_dir: 数据存储根目录（可以是相对路径或绝对路径）
        """
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_file_path(self, diary_date: date) -> Path:
        """获取指定日期的日记文件路径

        Args:
            diary_date: 日期

        Returns:
            文件路径，格式: base_dir/YYYY/YYYYMMDD.txt
        """
        filename = diary_date.strftime("%Y%m%d") + ".txt"
        return self.base_dir / str(diary_date.year) / filename

    def save(self, entry: DiaryEntry) -> None:
        """保存日记条目

        Args:
            entry: 日记条目
        """
        file_path = self.get_file_path(entry.date)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(entry.content)

        entry.file_path = file_path

    def load(self, diary_date: date) -> Optional[DiaryEntry]:
        """加载指定日期的日记

        Args:
            diary_date: 日期

        Returns:
            日记条目，如果不存在则返回 None
        """
        file_path = self.get_file_path(diary_date)
        if not file_path.exists():
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        entry = DiaryEntry(date=diary_date, content=content, file_path=file_path)
        return entry

    def delete(self, diary_date: date) -> bool:
        """删除指定日期的日记

        Args:
            diary_date: 日期

        Returns:
            是否成功删除
        """
        file_path = self.get_file_path(diary_date)
        if file_path.exists():
            file_path.unlink()
            # 清理空年份目录
            self._cleanup_empty_year_dir(diary_date.year)
            return True
        return False

    def exists(self, diary_date: date) -> bool:
        """检查日记是否存在

        Args:
            diary_date: 日期

        Returns:
            是否存在
        """
        return self.get_file_path(diary_date).exists()

    def list_all_entries(self) -> Iterator[DiaryEntry]:
        """遍历所有日记条目

        Yields:
            DiaryEntry: 日记条目，按日期排序
        """
        if not self.base_dir.exists():
            return

        for year_dir in sorted(self.base_dir.iterdir(), reverse=True):
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue

            for file_path in sorted(year_dir.iterdir()):
                if not file_path.is_file():
                    continue

                # 检查文件格式: YYYYMMDD.txt 或 YYYYMMDD.md
                name = file_path.stem
                if len(name) != 8 or not name.isdigit():
                    continue

                try:
                    diary_date = datetime.strptime(name, "%Y%m%d").date()
                    content = file_path.read_text(encoding="utf-8")
                    yield DiaryEntry(date=diary_date, content=content, file_path=file_path)
                except (ValueError, UnicodeDecodeError):
                    # 无效日期或编码错误，跳过
                    continue

    def list_entries_by_year(self, year: int) -> Iterator[DiaryEntry]:
        """遍历指定年份的日记条目

        Args:
            year: 年份

        Yields:
            DiaryEntry: 日记条目
        """
        year_dir = self.base_dir / str(year)
        if not year_dir.exists():
            return

        for file_path in sorted(year_dir.iterdir()):
            if not file_path.is_file():
                continue

            name = file_path.stem
            if len(name) != 8 or not name.isdigit():
                continue

            try:
                diary_date = datetime.strptime(name, "%Y%m%d").date()
                content = file_path.read_text(encoding="utf-8")
                yield DiaryEntry(date=diary_date, content=content, file_path=file_path)
            except (ValueError, UnicodeDecodeError):
                continue

    def list_entries_by_month(self, year: int, month: int) -> Iterator[DiaryEntry]:
        """遍历指定月份的日记条目

        Args:
            year: 年份
            month: 月份

        Yields:
            DiaryEntry: 日记条目
        """
        for entry in self.list_entries_by_year(year):
            if entry.month == month:
                yield entry

    def get_diary_dates(self, year: int, month: int) -> list[date]:
        """获取某月写了日记的所有日期

        Args:
            year: 年份
            month: 月份

        Returns:
            有日记的日期列表
        """
        dates = []
        for entry in self.list_entries_by_month(year, month):
            dates.append(entry.date)
        return sorted(dates)

    def get_all_years(self) -> list[int]:
        """获取所有有日记的年份

        Returns:
            年份列表（降序排列）
        """
        years = []
        if not self.base_dir.exists():
            return years

        for year_dir in self.base_dir.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit():
                years.append(int(year_dir.name))

        return sorted(years, reverse=True)

    def import_file(self, source_path: Path, dry_run: bool = False) -> tuple[bool, str]:
        """导入单个日记文件

        Args:
            source_path: 源文件路径
            dry_run: True 则只检查不导入

        Returns:
            (成功标志, 消息)
        """
        name = source_path.stem
        if len(name) != 8 or not name.isdigit():
            return False, f"跳过（文件名不符合 YYYYMMDD 格式）: {source_path.name}"

        try:
            diary_date = datetime.strptime(name, "%Y%m%d").date()
        except ValueError:
            return False, f"跳过（无效日期）: {source_path.name}"

        target_path = self.get_file_path(diary_date)

        if target_path.exists():
            return False, f"跳过（已存在）: {source_path.name}"

        if dry_run:
            return True, f"将导入: {source_path.name} -> {target_path}"

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        return True, f"已导入: {source_path.name}"

    def _cleanup_empty_year_dir(self, year: int) -> None:
        """清理空的年份目录"""
        year_dir = self.base_dir / str(year)
        if year_dir.exists() and year_dir.is_dir():
            # 检查是否为空目录
            if not any(year_dir.iterdir()):
                year_dir.rmdir()
