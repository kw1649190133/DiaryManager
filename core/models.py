"""数据模型"""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional


@dataclass
class DiaryEntry:
    """日记条目

    Attributes:
        date: 日记日期
        content: 日记内容（纯文本）
        file_path: 文件路径（可选，存储时自动设置）
        word_count: 字数统计（自动计算）
    """
    date: date
    content: str = ""
    file_path: Optional[Path] = None

    @property
    def word_count(self) -> int:
        """计算字数（中英文混合统计）"""
        if not self.content:
            return 0
        # 去除首尾空白后统计
        stripped = self.content.strip()
        if not stripped:
            return 0
        return len(stripped)

    @property
    def year(self) -> int:
        """获取年份"""
        return self.date.year

    @property
    def month(self) -> int:
        """获取月份"""
        return self.date.month

    @property
    def day(self) -> int:
        """获取日期"""
        return self.date.day

    def __repr__(self) -> str:
        return f"<DiaryEntry date={self.date} words={self.word_count}>"

    def __str__(self) -> str:
        return f"{self.date.strftime('%Y-%m-%d')} ({self.word_count}字)"


@dataclass
class DiaryStats:
    """日记统计信息"""
    total_days: int = 0  # 写了多少天
    total_words: int = 0  # 总字数
    avg_words_per_day: float = 0.0  # 平均每天字数
    longest_day: Optional[date] = None  # 字数最多的一天
    longest_words: int = 0  # 最长那天写了多少字
    shortest_day: Optional[date] = None  # 字数最少的一天
    shortest_words: int = 0  # 最短那天写了多少字
    entries: list[DiaryEntry] = field(default_factory=list)  # 所有日记条目


@dataclass
class MonthStats:
    """月度统计"""
    year: int
    month: int
    total_days: int = 0
    total_words: int = 0
    dates_with_entries: list[date] = field(default_factory=list)
