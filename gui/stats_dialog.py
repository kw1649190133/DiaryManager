"""统计对话框"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QDialog, QHBoxLayout,
    QLabel, QPushButton, QVBoxLayout
)

from core import DiaryManager


class StatsDialog(QDialog):
    """统计对话框"""

    def __init__(self, manager: DiaryManager, parent=None):
        super().__init__(parent)
        self.manager = manager

        self.setWindowTitle("日记统计")
        self.setMinimumSize(400, 320)
        self.resize(400, 320)

        self._init_ui()
        self._load_stats()

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # 顶部：年份选择
        top_bar = QHBoxLayout()

        year_label = QLabel("选择年份:")
        top_bar.addWidget(year_label)

        self.year_combo = QComboBox()
        self.year_combo.currentIndexChanged.connect(self._on_year_changed)
        top_bar.addWidget(self.year_combo)

        self.all_time_btn = QPushButton("全部时间")
        self.all_time_btn.clicked.connect(self._show_all_time)
        top_bar.addWidget(self.all_time_btn)

        top_bar.addStretch()

        layout.addLayout(top_bar)

        # 标题
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(self.title_label)

        # 统计内容区
        self.stats_container = QVBoxLayout()
        self.stats_container.setSpacing(12)
        layout.addLayout(self.stats_container)

        layout.addStretch()

        # 底部按钮
        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        bottom_bar.addWidget(close_btn)

        layout.addLayout(bottom_bar)

    def _load_stats(self):
        """加载统计"""
        years = self.manager.get_all_years()
        self.year_combo.blockSignals(True)  # 阻止信号触发
        self.year_combo.clear()

        if years:
            self.year_combo.addItem("全部时间", None)
            for year in years:
                self.year_combo.addItem(f"{year}年", year)
            self.year_combo.setCurrentIndex(1)
        else:
            self.year_combo.setCurrentIndex(0)

        self.year_combo.blockSignals(False)  # 恢复信号

        # 显示初始统计
        if years:
            self._show_stats_for_year(years[0])
        else:
            self._show_stats_for_year(None)

    def _show_all_time(self):
        """显示全部时间统计"""
        self.year_combo.setCurrentIndex(0)

    def _on_year_changed(self, index: int):
        """年份选择变化"""
        year = self.year_combo.currentData()
        self._show_stats_for_year(year)

    def _show_stats_for_year(self, year: Optional[int]):
        """显示统计"""
        # 清除现有内容
        while self.stats_container.count():
            item = self.stats_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 获取统计
        if year:
            stats = self.manager.get_year_stats(year)
            self.title_label.setText(f"{year}年统计")
        else:
            stats = self.manager.get_stats()
            self.title_label.setText("全部日记统计")

        # 写了几天
        self._add_stat_row(f"写了几天：{stats.total_days} 天")

        # 总字数
        self._add_stat_row(f"总字数：{stats.total_words} 字")

        # 平均每天字数
        avg = stats.avg_words_per_day
        self._add_stat_row(f"平均每天：{avg:.1f} 字" if avg > 0 else "平均每天：0 字")

        # 最多一天
        if stats.longest_day:
            self._add_stat_row(
                f"最多一天（{stats.longest_day.strftime('%Y-%m-%d')}）：{stats.longest_words} 字"
            )

        # 最少一天
        if stats.shortest_day:
            self._add_stat_row(
                f"最少一天（{stats.shortest_day.strftime('%Y-%m-%d')}）：{stats.shortest_words} 字"
            )

    def _add_stat_row(self, text: str):
        """添加一行统计文本"""
        label = QLabel(text)
        label.setStyleSheet("font-size: 12pt;")
        self.stats_container.addWidget(label)
