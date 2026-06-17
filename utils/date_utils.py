"""日期工具函数"""

from datetime import date, datetime


def parse_date_str(date_str: str) -> date:
    """解析日期字符串

    支持的格式:
    - YYYY-MM-DD (如 2024-01-15)
    - YYYYMMDD (如 20240115)

    Args:
        date_str: 日期字符串

    Returns:
        date 对象

    Raises:
        ValueError: 无法解析时抛出
    """
    formats = ["%Y-%m-%d", "%Y%m%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue

    raise ValueError(f"无法解析日期: {date_str}，支持的格式: YYYY-MM-DD, YYYYMMDD")


def format_date(date_obj: date, format: str = "%Y-%m-%d") -> str:
    """格式化日期

    Args:
        date_obj: date 对象
        format: 格式字符串

    Returns:
        格式化后的日期字符串
    """
    return date_obj.strftime(format)


def get_filename_from_date(date_obj: date) -> str:
    """从日期获取文件名

    Args:
        date_obj: date 对象

    Returns:
        文件名，如 "20240115.txt"
    """
    return date_obj.strftime("%Y%m%d") + ".txt"


def parse_date_from_filename(filename: str) -> date | None:
    """从文件名解析日期

    Args:
        filename: 文件名（可以是带路径的）

    Returns:
        date 对象，解析失败返回 None
    """
    from pathlib import Path

    name = Path(filename).stem
    if len(name) != 8 or not name.isdigit():
        return None

    try:
        return datetime.strptime(name, "%Y%m%d").date()
    except ValueError:
        return None


def get_month_range(year: int, month: int) -> tuple[date, date]:
    """获取月份的开始和结束日期

    Args:
        year: 年份
        month: 月份

    Returns:
        (开始日期, 结束日期)
    """
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)
    end = end.replace(day=end.day - 1) if end.day == 1 else end.replace(day=1) - __import__('datetime').timedelta(days=1)
    # 简化：直接计算月末
    if month == 12:
        end = date(year, 12, 31)
    else:
        end = date(year, month + 1, 1).__sub__(__import__('datetime').timedelta(days=1))
    return start, end


def get_weekday_name(weekday: int, short: bool = False) -> str:
    """获取星期几的名称

    Args:
        weekday: 星期几 (0=周一, 6=周日)
        short: 是否返回短名称

    Returns:
        星期名称
    """
    names_full = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    names_short = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    names = names_short if short else names_full
    return names[weekday % 7]


def is_valid_date_filename(filename: str) -> bool:
    """检查文件名是否为有效的日期格式

    Args:
        filename: 文件名

    Returns:
        是否有效
    """
    return parse_date_from_filename(filename) is not None
