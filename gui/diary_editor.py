"""日记编辑器组件"""

from datetime import date
from typing import Optional

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget
)


class DiaryEditor(QWidget):
    """日记编辑器

    Features:
        - 支持字体大小调整
        - 字数统计
        - 内容变化信号
    """

    content_changed = Signal()

    # 字体大小范围
    MIN_FONT_SIZE = 10
    MAX_FONT_SIZE = 32
    DEFAULT_FONT_SIZE = 14

    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.current_date: Optional[date] = None
        self.font_size = self.DEFAULT_FONT_SIZE
        self._has_diary = False
        self._is_dirty = False  # 是否有未保存的更改

        self._init_ui()
        self._apply_font_size()

    def _init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 工具栏
        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)

        # 文本编辑器
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("DiaryTextEdit")
        self.text_edit.setFrameShape(QFrame.NoFrame)
        self.text_edit.setAcceptRichText(False)
        self.text_edit.textChanged.connect(self._on_text_changed)

        self.scroll_area.setWidget(self.text_edit)
        layout.addWidget(self.scroll_area)

        # 底部信息栏
        status_bar = self._create_status_bar()
        layout.addWidget(status_bar)

    def _create_toolbar(self) -> QWidget:
        """创建工具栏"""
        toolbar = QFrame()
        toolbar.setObjectName("EditorToolbar")
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # 日期标签
        self.date_label = QLabel()
        self.date_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.date_label)

        layout.addStretch()

        # 字体大小控制
        font_label = QLabel("字号:")
        layout.addWidget(font_label)

        self.decrease_btn = QPushButton("A-")
        self.decrease_btn.setMaximumWidth(36)
        self.decrease_btn.setToolTip("减小字体 (Ctrl+-)")
        self.decrease_btn.clicked.connect(self._decrease_font_size)
        layout.addWidget(self.decrease_btn)

        self.font_size_label = QLabel(f"{self.font_size}")
        self.font_size_label.setAlignment(Qt.AlignCenter)
        self.font_size_label.setMinimumWidth(30)
        layout.addWidget(self.font_size_label)

        self.increase_btn = QPushButton("A+")
        self.increase_btn.setMaximumWidth(36)
        self.increase_btn.setToolTip("增大字体 (Ctrl++)")
        self.increase_btn.clicked.connect(self._increase_font_size)
        layout.addWidget(self.increase_btn)

        return toolbar

    def _create_status_bar(self) -> QWidget:
        """创建状态栏"""
        status_bar = QFrame()
        status_bar.setObjectName("EditorStatusBar")
        layout = QHBoxLayout(status_bar)
        layout.setContentsMargins(12, 4, 12, 4)

        self.word_count_label = QLabel("0 字")
        layout.addWidget(self.word_count_label)

        layout.addStretch()

        self.diary_status_label = QLabel()
        layout.addWidget(self.diary_status_label)

        return status_bar

    def _apply_font_size(self):
        """应用字体大小 — 通过样式表控制字号，优先级高于主窗口样式表"""
        # 使用子控件样式表直接设置字号，确保不受主窗口样式表影响
        self.text_edit.setStyleSheet(
            f"#DiaryTextEdit {{ font-size: {self.font_size}pt; font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif; line-height: 1.8; }}"
        )
        self.font_size_label.setText(str(self.font_size))

        # 更新按钮状态
        self.decrease_btn.setEnabled(self.font_size > self.MIN_FONT_SIZE)
        self.increase_btn.setEnabled(self.font_size < self.MAX_FONT_SIZE)

    def _increase_font_size(self):
        """增大字体"""
        if self.font_size < self.MAX_FONT_SIZE:
            self.font_size += 1
            self._apply_font_size()

    def _decrease_font_size(self):
        """减小字体"""
        if self.font_size > self.MIN_FONT_SIZE:
            self.font_size -= 1
            self._apply_font_size()

    def set_content(self, diary_date: date, content: str, has_diary: bool = True):
        """设置编辑器内容

        Args:
            diary_date: 日期
            content: 内容
            has_diary: 是否有日记
        """
        self.current_date = diary_date
        self._has_diary = has_diary
        self._is_dirty = False  # 重置未保存标志

        # 更新日期标签
        weekday_names = ["一", "二", "三", "四", "五", "六", "日"]
        weekday = weekday_names[diary_date.weekday()]
        self.date_label.setText(f"{diary_date.strftime('%Y年%m月%d日')} 星期{weekday}")

        # 设置内容
        self.text_edit.setPlainText(content)
        self._update_word_count()

        # 更新状态
        if has_diary:
            self.diary_status_label.setText("已有日记")
        else:
            self.diary_status_label.setText("新建日记")

    def get_content(self) -> str:
        """获取编辑器内容"""
        return self.text_edit.toPlainText()

    def get_word_count(self) -> int:
        """获取字数"""
        content = self.text_edit.toPlainText().strip()
        return len(content) if content else 0

    def clear(self):
        """清空编辑器"""
        self.text_edit.clear()
        self.current_date = None
        self._has_diary = False
        self.date_label.setText("")
        self.word_count_label.setText("0 字")
        self.diary_status_label.setText("")

    def _update_word_count(self):
        """更新字数统计"""
        count = self.get_word_count()
        self.word_count_label.setText(f"{count} 字")

    def _on_text_changed(self):
        """文本变化"""
        self._update_word_count()
        self._is_dirty = True  # 标记为有未保存的更改
        self.content_changed.emit()

    def is_dirty(self) -> bool:
        """检查是否有未保存的更改"""
        return self._is_dirty

    def mark_saved(self):
        """标记为已保存"""
        self._is_dirty = False

    def zoom_in(self):
        """放大（快捷方式）"""
        self._increase_font_size()

    def zoom_out(self):
        """缩小（快捷方式）"""
        self._decrease_font_size()
