"""日历视图组件"""

from datetime import date
from typing import Optional

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import (
    QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget, QMessageBox
)


class DateCell(QWidget):
    """日期单元格

    Attributes:
        hasDiary: 是否有日记
        isToday: 是否是今天
        isSelected: 是否被选中
    """

    clicked = Signal(date)

    def __init__(self, diary_date: date, parent=None):
        super().__init__(parent)
        self.diary_date = diary_date
        self.hasDiary = False
        self.isToday = False
        self.isSelected = False
        self._is_hovered = False

        self.setMinimumSize(36, 36)
        self.setMaximumSize(50, 50)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAttribute(Qt.WA_Hover, True)  # 启用 hover 事件

    def set_state(self, has_diary: bool, is_today: bool, is_selected: bool):
        """一次性设置所有状态并刷新"""
        self.hasDiary = has_diary
        self.isToday = is_today
        self.isSelected = is_selected
        self.update()

    def _adjust_color(self, color: QColor, brightness: float) -> QColor:
        """调整颜色亮度"""
        r = min(255, int(color.red() * brightness))
        g = min(255, int(color.green() * brightness))
        b = min(255, int(color.blue() * brightness))
        return QColor(r, g, b)

    def paintEvent(self, event):
        """自定义绘制：圆形背景 + 日期文字"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(2, 2, -2, -2)

        # 悬停时增加亮度
        hover_brightness = 1.15 if self._is_hovered else 1.0

        if self.isSelected:
            # 选中：蓝色实心圆
            painter.setBrush(QColor("#0078d4"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(rect)
        elif self.hasDiary and self.isToday:
            # 有日记且是今天：绿底蓝边
            painter.setBrush(self._adjust_color(QColor("#dff6dd"), hover_brightness))
            painter.setPen(QPen(QColor("#0078d4"), 2))
            painter.drawEllipse(rect)
        elif self.hasDiary:
            # 有日记：绿底绿边
            painter.setBrush(self._adjust_color(QColor("#dff6dd"), hover_brightness))
            painter.setPen(QPen(QColor("#107c10"), 2))
            painter.drawEllipse(rect)
        elif self.isToday:
            # 今天无日记：透明底蓝边
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor("#0078d4"), 2))
            painter.drawEllipse(rect)
        elif self._is_hovered:
            # 普通日期悬停：浅灰底
            painter.setBrush(QColor("#e8e8e8"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(rect)

        # 绘制日期文字
        text_color = "white" if self.isSelected else "#323130"
        painter.setPen(QColor(text_color))
        painter.drawText(self.rect(), Qt.AlignCenter, str(self.diary_date.day))

    def mousePressEvent(self, event):
        """鼠标点击"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.diary_date)

    def enterEvent(self, event):
        """鼠标进入"""
        self._is_hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开"""
        self._is_hovered = False
        self.update()
        super().leaveEvent(event)


class CalendarView(QWidget):
    """日历视图组件

    Signals:
        date_selected: 选择日期时发出
        create_diary_requested: 请求创建日记时发出
    """

    date_selected = Signal(date)

    WEEKDAY_NAMES = ["一", "二", "三", "四", "五", "六", "日"]

    def __init__(self, calendar_service, parent=None):
        super().__init__(parent)
        self.setObjectName("CalendarPanel")
        self.calendar_service = calendar_service
        self.current_year = date.today().year
        self.current_month = date.today().month
        self.selected_date: Optional[date] = None

        self._init_ui()
        self.refresh()

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # 标题栏
        header = self._create_header()
        layout.addWidget(header)

        # 星期标题
        weekday_bar = self._create_weekday_bar()
        layout.addWidget(weekday_bar)

        # 日历网格
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(4)
        layout.addLayout(self.grid_layout)

        # 信息栏
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 9pt;")
        layout.addWidget(self.info_label)

        layout.addStretch()

    def _create_header(self) -> QWidget:
        """创建标题栏"""
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # 第一行：年份快速跳转
        year_nav = QWidget()
        year_nav_layout = QHBoxLayout(year_nav)
        year_nav_layout.setContentsMargins(0, 0, 0, 0)

        btn_minus_10 = QPushButton("<<")
        btn_minus_10.setToolTip("上10年")
        btn_minus_10.setMaximumWidth(36)
        btn_minus_10.clicked.connect(self._on_prev_10_years)
        year_nav_layout.addWidget(btn_minus_10)

        btn_minus_1 = QPushButton("<")
        btn_minus_1.setToolTip("上一年")
        btn_minus_1.setMaximumWidth(36)
        btn_minus_1.clicked.connect(self._on_prev_year)
        year_nav_layout.addWidget(btn_minus_1)

        self.year_input = QLineEdit()
        self.year_input.setMaxLength(4)
        self.year_input.setMaximumWidth(60)
        self.year_input.setAlignment(Qt.AlignCenter)
        self.year_input.setPlaceholderText("年份")
        self.year_input.returnPressed.connect(self._on_year_input_enter)
        year_nav_layout.addWidget(self.year_input)

        btn_plus_1 = QPushButton(">")
        btn_plus_1.setToolTip("下一年")
        btn_plus_1.setMaximumWidth(36)
        btn_plus_1.clicked.connect(self._on_next_year)
        year_nav_layout.addWidget(btn_plus_1)

        btn_plus_10 = QPushButton(">>")
        btn_plus_10.setToolTip("下10年")
        btn_plus_10.setMaximumWidth(36)
        btn_plus_10.clicked.connect(self._on_next_10_years)
        year_nav_layout.addWidget(btn_plus_10)

        layout.addWidget(year_nav)

        # 第二行：月份导航
        month_nav = QWidget()
        month_nav_layout = QHBoxLayout(month_nav)
        month_nav_layout.setContentsMargins(0, 0, 0, 0)

        self.prev_btn = QPushButton("◀")
        self.prev_btn.setToolTip("上一月")
        self.prev_btn.setMaximumWidth(36)
        self.prev_btn.clicked.connect(self._on_prev_month)
        month_nav_layout.addWidget(self.prev_btn)

        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        month_nav_layout.addWidget(self.month_label)

        self.next_btn = QPushButton("▶")
        self.next_btn.setToolTip("下一月")
        self.next_btn.setMaximumWidth(36)
        self.next_btn.clicked.connect(self._on_next_month)
        month_nav_layout.addWidget(self.next_btn)

        layout.addWidget(month_nav)

        return header

    def _create_weekday_bar(self) -> QWidget:
        """创建星期标题栏"""
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(4)

        for name in self.WEEKDAY_NAMES:
            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold;")
            layout.addWidget(label)

        return bar

    def set_date(self, year: int, month: int):
        """设置显示的年月"""
        self.current_year = year
        self.current_month = month
        self.refresh()

    def refresh(self):
        """刷新日历"""
        # 更新标题
        self.month_label.setText(f"{self.current_year}年 {self.current_month}月")
        self.year_input.setText(str(self.current_year))

        # 获取数据
        data = self.calendar_service.get_month_calendar_data(self.current_year, self.current_month)

        # 清除现有单元格
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 创建新单元格
        today = date.today()
        diary_dates = set(data["diary_dates"])

        row = 0
        for week in data["weeks"]:
            col = 0
            for day_data in week:
                if day_data is None:
                    # 空白格子
                    spacer = QWidget()
                    spacer.setMinimumSize(36, 36)
                    self.grid_layout.addWidget(spacer, row, col)
                else:
                    diary_date = day_data["date"]
                    has_diary = diary_date in diary_dates

                    cell = DateCell(diary_date)
                    cell.set_state(
                        has_diary=has_diary,
                        is_today=(diary_date == today),
                        is_selected=(diary_date == self.selected_date)
                    )
                    cell.clicked.connect(self._on_cell_clicked)

                    self.grid_layout.addWidget(cell, row, col)

                col += 1
            row += 1

        # 更新信息栏
        missing_count = len(data["missing_dates"])
        diary_count = len(data["diary_dates"])
        total_days = data["days_in_month"]

        info_text = f"📝 本月写了 {diary_count} 天"
        if missing_count > 0:
            info_text += f" | ❌ 未写 {missing_count} 天"

        self.info_label.setText(info_text)

    def select_date(self, diary_date: date):
        """选中日期"""
        self.selected_date = diary_date

        # 如果选中日期不在当前月份，切换月份
        if diary_date.year != self.current_year or diary_date.month != self.current_month:
            self.current_year = diary_date.year
            self.current_month = diary_date.month
            self.refresh()
        else:
            # 只更新选中状态
            self.refresh()

    @Slot(date)
    def _on_cell_clicked(self, diary_date: date):
        """单元格点击 — 直接跳转，不自动创建日记"""
        self.selected_date = diary_date
        self.date_selected.emit(diary_date)

    def _on_prev_month(self):
        """上一个月"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.refresh()

    def _on_next_month(self):
        """下一个月"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.refresh()

    def _on_prev_year(self):
        """上一年"""
        self.current_year -= 1
        self.refresh()

    def _on_next_year(self):
        """下一年"""
        self.current_year += 1
        self.refresh()

    def _on_prev_10_years(self):
        """上10年"""
        self.current_year -= 10
        self.refresh()

    def _on_next_10_years(self):
        """下10年"""
        self.current_year += 10
        self.refresh()

    def _on_year_input_enter(self):
        """年份输入框回车跳转"""
        text = self.year_input.text().strip()
        try:
            year = int(text)
            if 1900 <= year <= 2100:
                self.current_year = year
                self.refresh()
            else:
                QMessageBox.warning(self, "无效年份", "请输入1900-2100之间的年份")
                self.year_input.setText(str(self.current_year))
        except ValueError:
            QMessageBox.warning(self, "无效输入", "请输入有效的年份数字")
            self.year_input.setText(str(self.current_year))
