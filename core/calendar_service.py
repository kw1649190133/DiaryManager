"""日历服务 - 提供日历视图相关的数据查询"""

from datetime import date, timedelta
from typing import Set

from .storage import FileDiaryStorage


class CalendarService:
    """日历服务

    提供日历视图所需的数据查询功能。
    核心层独立，不依赖任何 UI 框架。
    """

    def __init__(self, storage: FileDiaryStorage):
        """初始化日历服务

        Args:
            storage: 存储实例
        """
        self.storage = storage

    def get_diary_dates(self, year: int, month: int) -> list[date]:
        """获取某月写了日记的所有日期

        Args:
            year: 年份
            month: 月份

        Returns:
            有日记的日期列表（已排序）
        """
        return self.storage.get_diary_dates(year, month)

    def get_diary_dates_set(self, year: int, month: int) -> Set[date]:
        """获取某月写了日记的所有日期（Set 版本，便于快速查找）

        Args:
            year: 年份
            month: 月份

        Returns:
            有日记的日期集合
        """
        return set(self.storage.get_diary_dates(year, month))

    def get_missing_dates(self, year: int, month: int) -> list[date]:
        """获取某月没有写日记的所有日期

        Args:
            year: 年份
            month: 月份

        Returns:
            没有日记的日期列表
        """
        diary_dates = self.get_diary_dates_set(year, month)
        missing = []

        # 获取该月的第一天和最后一天
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)

        current = first_day
        while current <= last_day:
            if current not in diary_dates:
                missing.append(current)
            current += timedelta(days=1)

        return missing

    def has_diary(self, diary_date: date) -> bool:
        """检查指定日期是否有日记

        Args:
            diary_date: 日期

        Returns:
            是否有日记
        """
        return self.storage.exists(diary_date)

    def get_month_calendar_data(self, year: int, month: int) -> dict:
        """获取日历视图所需的完整数据

        Args:
            year: 年份
            month: 月份

        Returns:
            包含以下键的字典:
            - diary_dates: 有日记的日期列表
            - missing_dates: 没写日记的日期列表
            - first_weekday: 该月第一天是星期几 (0=周一, 6=周日)
            - days_in_month: 该月总天数
            - weeks: 日历网格数据，每行是一周的日期
        """
        diary_dates_set = self.get_diary_dates_set(year, month)

        # 获取该月的第一天和最后一天
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)

        days_in_month = last_day.day

        # 构建日历网格
        # ISO 周历: 周一=0, 周日=6
        first_weekday = first_day.weekday()

        weeks = []
        current_day = 1
        current = first_day

        # 填充第一周前面的空白
        week = [None] * first_weekday

        while current_day <= days_in_month:
            if len(week) == 7:
                weeks.append(week)
                week = []

            week.append({
                "date": current,
                "day": current_day,
                "has_diary": current in diary_dates_set
            })
            current_day += 1
            current += timedelta(days=1)

        # 填充最后一周的空白
        while len(week) < 7:
            week.append(None)

        if week:
            weeks.append(week)

        # 计算没有写日记的日期
        missing_dates = [d for d in range(1, days_in_month + 1)
                         if date(year, month, d) not in diary_dates_set]

        return {
            "year": year,
            "month": month,
            "diary_dates": sorted(diary_dates_set),
            "missing_dates": missing_dates,
            "first_weekday": first_weekday,
            "days_in_month": days_in_month,
            "weeks": weeks
        }

    def get_recent_diary_dates(self, count: int = 10) -> list[date]:
        """获取最近的日记日期

        Args:
            count: 返回数量

        Returns:
            最近的日记日期列表（降序）
        """
        entries = list(self.storage.list_all_entries())
        entries.sort(key=lambda e: e.date, reverse=True)
        return [e.date for e in entries[:count]]

    def get_streak_info(self) -> dict:
        """获取连续写日记的信息

        Returns:
            包含:
            - current_streak: 当前连续天数
            - longest_streak: 最长连续天数
            - last_diary_date: 最近一次写日记的日期
        """
        entries = list(self.storage.list_all_entries())
        if not entries:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "last_diary_date": None
            }

        # 按日期排序
        entries.sort(key=lambda e: e.date)
        diary_dates = [e.date for e in entries]
        last_date = diary_dates[-1]

        # 计算当前连续天数（从最后一天往前数）
        current_streak = 0
        today = date.today()
        check_date = last_date

        while check_date >= last_date and check_date <= today:
            if check_date in diary_dates:
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break

        # 计算最长连续天数
        longest_streak = 0
        streak = 1

        for i in range(1, len(diary_dates)):
            if (diary_dates[i] - diary_dates[i - 1]).days == 1:
                streak += 1
            else:
                longest_streak = max(longest_streak, streak)
                streak = 1

        longest_streak = max(longest_streak, streak)

        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_diary_date": last_date
        }
