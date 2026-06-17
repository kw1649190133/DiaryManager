"""样式表定义 — 浅色主题与深色主题"""


# ═══════════════════════════════════════════════════════════════
# 浅色主题（默认）
# ═══════════════════════════════════════════════════════════════

def get_light_style() -> str:
    return """
/* ── 全局 ── */
QMainWindow {
    background-color: #f3f3f3;
    color: #1e1e1e;
}

QWidget {
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    font-size: 10pt;
    color: #1e1e1e;
}

/* ── 按钮 ── */
QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 14px;
    min-width: 60px;
}
QPushButton:hover { background-color: #106ebe; }
QPushButton:pressed { background-color: #005a9e; }
QPushButton:disabled { background-color: #cccccc; color: #888888; }

QPushButton#secondary {
    background-color: transparent;
    color: #0078d4;
    border: 1px solid #0078d4;
}
QPushButton#secondary:hover { background-color: #e8f4fd; }

QPushButton#danger { background-color: #d13438; }
QPushButton#danger:hover { background-color: #a4262c; }

/* ── 输入框 ── */
QLineEdit, QTextEdit {
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 6px 10px;
    background-color: white;
    color: #1e1e1e;
    selection-background-color: #0078d4;
}
QLineEdit:focus, QTextEdit:focus { border: 2px solid #0078d4; }

/* ── 标签 ── */
QLabel { color: #1e1e1e; }
QLabel#title { font-size: 14pt; font-weight: bold; color: #1e1e1e; }
QLabel#subtitle { font-size: 11pt; color: #666666; }

/* ── 框架 ── */
QFrame#card {
    background-color: white;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}

/* ── 列表 ── */
QListWidget {
    border: 1px solid #d0d0d0;
    background-color: white;
    border-radius: 4px;
}
QListWidget::item { padding: 6px; border-radius: 4px; }
QListWidget::item:selected { background-color: #e8f4fd; color: #1e1e1e; }
QListWidget::item:hover { background-color: #f0f0f0; }

/* ── 状态栏 ── */
QStatusBar {
    background-color: #f0f0f0;
    border-top: 1px solid #d0d0d0;
    color: #555555;
}
QStatusBar::item { border: none; }

/* ── 滚动条 ── */
QScrollBar:vertical { width: 8px; background: transparent; }
QScrollBar::handle:vertical {
    background: #c0c0c0; border-radius: 4px; min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #a0a0a0; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

QScrollBar:horizontal { height: 8px; background: transparent; }
QScrollBar::handle:horizontal {
    background: #c0c0c0; border-radius: 4px; min-width: 30px;
}
QScrollBar::handle:horizontal:hover { background: #a0a0a0; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }

/* ── 工具栏 ── */
QToolBar {
    background-color: white;
    border: none;
    border-bottom: 1px solid #e0e0e0;
    spacing: 6px;
    padding: 4px;
}
QToolBar:separator { width: 1px; background: #e0e0e0; margin: 4px 6px; }

QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 5px 8px;
    color: #1e1e1e;
}
QToolButton:hover { background-color: #e8f4fd; }
QToolButton:pressed { background-color: #d0e8fa; }

/* ── 菜单栏 ── */
QMenuBar {
    background-color: white;
    border-bottom: 1px solid #e0e0e0;
    color: #1e1e1e;
}
QMenuBar::item {
    padding: 5px 10px;
    background: transparent;
}
QMenuBar::item:selected { background-color: #e8f4fd; }
QMenuBar::item:pressed { background-color: #d0e8fa; }

QMenu {
    background-color: white;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    color: #1e1e1e;
}
QMenu::item { padding: 6px 24px 6px 20px; }
QMenu::item:selected { background-color: #e8f4fd; }
QMenu::separator { height: 1px; background: #e0e0e0; margin: 4px 0; }

/* ── 对话框 ── */
QDialog { background-color: #f3f3f3; color: #1e1e1e; }

/* ── ComboBox ── */
QComboBox {
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 4px 10px;
    background-color: white;
    color: #1e1e1e;
}
QComboBox:hover { border-color: #0078d4; }
QComboBox:focus { border: 2px solid #0078d4; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #888; }
QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #d0d0d0;
    selection-background-color: #e8f4fd;
    color: #1e1e1e;
}

/* ── 日历视图 ── */
#CalendarPanel {
    background-color: white;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}

#CalendarPanel QLabel {
    color: #1e1e1e;
}

/* ── 编辑器 ── */
#EditorToolbar {
    background-color: white;
    border-bottom: 1px solid #e0e0e0;
}

#EditorStatusBar {
    background-color: #f0f0f0;
    border-top: 1px solid #e0e0e0;
}

#DiaryTextEdit {
    border: none;
    padding: 16px 20px;
    background-color: white;
    color: #1a1a1a;
    selection-background-color: #0078d4;
    selection-color: white;
    line-height: 1.8;
}

/* ── 统计卡片 ── */
StatCard, QFrame#StatCard {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}
"""


# ═══════════════════════════════════════════════════════════════
# 深色主题
# ═══════════════════════════════════════════════════════════════

def get_dark_style() -> str:
    return """
/* ── 全局 ── */
QMainWindow {
    background-color: #1e1e1e;
    color: #d4d4d4;
}

QWidget {
    font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
    font-size: 10pt;
    color: #d4d4d4;
}

/* ── 按钮 ── */
QPushButton {
    background-color: #3c3c3c;
    color: #d4d4d4;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px 14px;
    min-width: 60px;
}
QPushButton:hover { background-color: #4a4a4a; border-color: #777777; }
QPushButton:pressed { background-color: #2d2d2d; }
QPushButton:disabled { background-color: #2a2a2a; color: #666666; border-color: #3a3a3a; }

QPushButton#secondary {
    background-color: transparent;
    color: #60a5fa;
    border: 1px solid #60a5fa;
}
QPushButton#secondary:hover { background-color: #1a2a3a; }

QPushButton#danger { background-color: #8b2222; border-color: #a03030; }
QPushButton#danger:hover { background-color: #a03030; }

/* ── 输入框 ── */
QLineEdit, QTextEdit {
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 6px 10px;
    background-color: #2d2d2d;
    color: #d4d4d4;
    selection-background-color: #60a5fa;
    selection-color: #1e1e1e;
}
QLineEdit:focus, QTextEdit:focus { border: 2px solid #60a5fa; }

/* ── 标签 ── */
QLabel { color: #d4d4d4; }
QLabel#title { font-size: 14pt; font-weight: bold; color: #e0e0e0; }
QLabel#subtitle { font-size: 11pt; color: #909090; }

/* ── 框架 ── */
QFrame#card {
    background-color: #2a2a2a;
    border-radius: 8px;
    border: 1px solid #3a3a3a;
}

/* ── 列表 ── */
QListWidget {
    border: 1px solid #3c3c3c;
    background-color: #2d2d2d;
    border-radius: 4px;
}
QListWidget::item { padding: 6px; border-radius: 4px; color: #d4d4d4; }
QListWidget::item:selected { background-color: #1a3a5a; color: #e0e0e0; }
QListWidget::item:hover { background-color: #383838; }

/* ── 状态栏 ── */
QStatusBar {
    background-color: #232323;
    border-top: 1px solid #3a3a3a;
    color: #888888;
}
QStatusBar::item { border: none; }

/* ── 滚动条 ── */
QScrollBar:vertical { width: 8px; background: transparent; }
QScrollBar::handle:vertical {
    background: #555555; border-radius: 4px; min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #666666; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

QScrollBar:horizontal { height: 8px; background: transparent; }
QScrollBar::handle:horizontal {
    background: #555555; border-radius: 4px; min-width: 30px;
}
QScrollBar::handle:horizontal:hover { background: #666666; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }

/* ── 工具栏 ── */
QToolBar {
    background-color: #252525;
    border: none;
    border-bottom: 1px solid #3a3a3a;
    spacing: 6px;
    padding: 4px;
}
QToolBar:separator { width: 1px; background: #3a3a3a; margin: 4px 6px; }

QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 5px 8px;
    color: #d4d4d4;
}
QToolButton:hover { background-color: #333333; }
QToolButton:pressed { background-color: #2a2a2a; }

/* ── 菜单栏 ── */
QMenuBar {
    background-color: #252525;
    border-bottom: 1px solid #3a3a3a;
    color: #d4d4d4;
}
QMenuBar::item {
    padding: 5px 10px;
    background: transparent;
}
QMenuBar::item:selected { background-color: #333333; }
QMenuBar::item:pressed { background-color: #2a2a2a; }

QMenu {
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #d4d4d4;
}
QMenu::item { padding: 6px 24px 6px 20px; }
QMenu::item:selected { background-color: #333333; }
QMenu::separator { height: 1px; background: #3a3a3a; margin: 4px 0; }

/* ── 对话框 ── */
QDialog { background-color: #1e1e1e; color: #d4d4d4; }

/* ── ComboBox ── */
QComboBox {
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 4px 10px;
    background-color: #2d2d2d;
    color: #d4d4d4;
}
QComboBox:hover { border-color: #60a5fa; }
QComboBox:focus { border: 2px solid #60a5fa; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #888;
}
QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #3c3c3c;
    selection-background-color: #1a3a5a;
    color: #d4d4d4;
}

/* ── 日历视图 ── */
#CalendarPanel {
    background-color: #2a2a2a;
    border-radius: 8px;
    border: 1px solid #3a3a3a;
}

#CalendarPanel QLabel {
    color: #d4d4d4;
}

/* ── 编辑器 ── */
#EditorToolbar {
    background-color: #252525;
    border-bottom: 1px solid #3a3a3a;
}

#EditorStatusBar {
    background-color: #232323;
    border-top: 1px solid #3a3a3a;
}

#DiaryTextEdit {
    border: none;
    padding: 16px 20px;
    background-color: #1e1e1e;
    color: #d4d4d4;
    selection-background-color: #60a5fa;
    selection-color: #1e1e1e;
    line-height: 1.8;
}

/* ── 统计卡片 ── */
StatCard, QFrame#StatCard {
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
}
"""


# ── 向后兼容：旧的 MAIN_STYLE 等同于浅色主题 ──
MAIN_STYLE = get_light_style()
CALENDAR_STYLE = ""
EDITOR_STYLE = ""
STATS_STYLE = ""
