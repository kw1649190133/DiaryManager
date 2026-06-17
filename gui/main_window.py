"""主窗口"""

from datetime import date
from typing import Optional

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel,
    QMainWindow, QMessageBox, QMenuBar, QPushButton, QSplitter,
    QStatusBar, QVBoxLayout, QWidget
)

from core import DiaryManager, CalendarService
from .calendar_view import CalendarView
from .diary_editor import DiaryEditor
from .stats_dialog import StatsDialog
from .styles import get_light_style, get_dark_style


class MainWindow(QMainWindow):
    """日记本主窗口"""

    # 信号
    diary_saved = Signal(date)  # 日记保存时发出
    diary_deleted = Signal(date)  # 日记删除时发出

    def __init__(self, data_dir: str = "data"):
        super().__init__()
        self.data_dir = data_dir

        # 主题状态: True = 深色, False = 浅色
        self._is_dark_theme = False

        # 初始化核心模块
        self.manager = DiaryManager()
        self.calendar_service = CalendarService(self.manager.storage)

        # 当前选中的日期
        self.current_date: Optional[date] = None

        self._init_ui()
        self._init_connections()
        self._apply_theme()  # 应用默认主题

        # 启动时自动导入
        self._auto_import_on_startup()

        # 默认显示今天
        today = date.today()
        self.calendar_view.set_date(today.year, today.month)
        self.select_date(today)

    def _init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("我的日记本")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # 左侧面板
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        # 右侧编辑器
        self.editor = DiaryEditor(self.manager)
        splitter.addWidget(self.editor)

        # 创建菜单栏
        self._create_menubar()

        # 创建工具栏
        self._create_toolbar()

        # 创建状态栏
        self._create_statusbar()

    def _create_menubar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件(F)")

        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._on_save_diary)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        refresh_menu_action = QAction("刷新日历", self)
        refresh_menu_action.setShortcut("F5")
        refresh_menu_action.triggered.connect(self._on_refresh)
        file_menu.addAction(refresh_menu_action)

        file_menu.addSeparator()

        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 视图菜单
        view_menu = menubar.addMenu("视图(V)")

        self.theme_action = QAction("深色主题", self)
        self.theme_action.setCheckable(True)
        self.theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(self.theme_action)

        view_menu.addSeparator()

        zoom_in_action = QAction("放大字体", self)
        zoom_in_action.setShortcut("Ctrl+=")
        zoom_in_action.triggered.connect(lambda: self.editor.zoom_in())
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("缩小字体", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(lambda: self.editor.zoom_out())
        view_menu.addAction(zoom_out_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助(H)")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_left_panel(self) -> QWidget:
        """创建左侧面板"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(8)

        # 日历视图
        self.calendar_view = CalendarView(self.calendar_service)
        self.calendar_view.date_selected.connect(self.select_date)
        layout.addWidget(self.calendar_view)

        # 统计按钮
        stats_btn = QPushButton("统计数据")
        stats_btn.setObjectName("secondary")
        stats_btn.clicked.connect(self.show_stats)
        layout.addWidget(stats_btn)

        return left_widget

    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar("工具栏")
        toolbar.setMovable(False)

        # 新建按钮
        new_action = QAction("新建日记", self)
        new_action.triggered.connect(self._on_new_diary)
        toolbar.addAction(new_action)

        toolbar.addSeparator()

        # 保存按钮
        save_action = QAction("保存", self)
        save_action.triggered.connect(self._on_save_diary)
        toolbar.addAction(save_action)

        # 删除按钮
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self._on_delete_diary)
        toolbar.addAction(delete_action)

        toolbar.addSeparator()

        # 刷新按钮
        refresh_action = QAction("刷新", self)
        refresh_action.setToolTip("刷新日历（F5）")
        refresh_action.triggered.connect(self._on_refresh)
        toolbar.addAction(refresh_action)

        toolbar.addSeparator()

        # 搜索按钮
        search_action = QAction("搜索", self)
        search_action.triggered.connect(self._on_search)
        toolbar.addAction(search_action)

        # 统计按钮
        stats_action = QAction("统计", self)
        stats_action.triggered.connect(self.show_stats)
        toolbar.addAction(stats_action)

        # 主题切换按钮
        toolbar.addSeparator()
        self.theme_btn = QPushButton("深色")
        self.theme_btn.setMaximumWidth(60)
        self.theme_btn.setToolTip("切换深色/浅色主题")
        self.theme_btn.clicked.connect(self._toggle_theme)
        toolbar.addWidget(self.theme_btn)

    def _create_statusbar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("就绪")
        self.status_bar.addPermanentWidget(self.status_label)

    def _init_connections(self):
        """初始化信号连接"""
        self.editor.content_changed.connect(self._on_content_changed)
        self.diary_saved.connect(self._on_diary_saved)
        self.diary_deleted.connect(self._on_diary_deleted)

    def _apply_theme(self):
        """应用当前主题样式"""
        if self._is_dark_theme:
            style = get_dark_style()
            self.theme_action.setText("浅色主题")
            self.theme_action.setChecked(True)
            self.theme_btn.setText("浅色")
        else:
            style = get_light_style()
            self.theme_action.setText("深色主题")
            self.theme_action.setChecked(False)
            self.theme_btn.setText("深色")

        self.setStyleSheet(style)

    def _toggle_theme(self):
        """切换深色/浅色主题"""
        self._is_dark_theme = not self._is_dark_theme
        self._apply_theme()

    def _show_about(self):
        """显示关于"""
        QMessageBox.about(
            self,
            "关于",
            "我的日记本 v1.4\n\n"
            "一个简洁的本地日记管理工具。\n"
            "数据以纯文本格式存储在 data/ 目录下。"
        )

    def _auto_import_on_startup(self):
        """启动时自动导入"""
        result = self.manager.auto_import()
        if result["imported"] > 0:
            self.status_bar.showMessage(f"已自动导入 {result['imported']} 篇日记", 5000)
            self.calendar_view.refresh()

    @Slot(date)
    def select_date(self, diary_date: date):
        """选中日期"""
        # 如果有未保存的更改，先自动保存
        self._auto_save_if_needed()

        self.current_date = diary_date

        # 加载日记内容
        entry = self.manager.load(diary_date)
        if entry:
            self.editor.set_content(diary_date, entry.content)
        else:
            self.editor.set_content(diary_date, "", has_diary=False)

        # 更新日历选中状态
        self.calendar_view.select_date(diary_date)

        # 更新状态栏
        word_count = self.editor.get_word_count()
        status = f"正在查看: {diary_date.strftime('%Y-%m-%d')} ({word_count}字)"
        self.status_label.setText(status)

    @Slot()
    def create_diary(self):
        """创建日记（已废弃，保留兼容性）"""
        pass

    def _on_new_diary(self):
        """新建日记 — 为当前选中日期新建；若无选中则为今天"""
        target = self.current_date if self.current_date else date.today()
        try:
            self.manager.create(target, "")
            # 先更新 is_dirty = False 避免触发自动保存覆盖新文件
            self.editor.mark_saved()
            self.select_date(target)
            self.calendar_view.set_date(target.year, target.month)
            self.status_label.setText(f"已新建: {target.strftime('%Y-%m-%d')}")
        except FileExistsError:
            QMessageBox.information(self, "提示", f"{target.strftime('%Y-%m-%d')} 的日记已存在")

    def _on_save_diary(self):
        """保存日记"""
        if self.current_date is None:
            QMessageBox.warning(self, "提示", "请先选择一个日期")
            return

        content = self.editor.get_content()
        entry = self.manager.save(self.current_date, content)
        self.editor.mark_saved()  # 标记为已保存
        self.diary_saved.emit(self.current_date)
        self.calendar_view.refresh()

        word_count = entry.word_count
        self.status_label.setText(f"已保存: {self.current_date.strftime('%Y-%m-%d')} ({word_count}字)")

    def _auto_save_if_needed(self):
        """如果有未保存的更改，自动保存（内容为空时不保存，避免为无日记的日期创建空文件）"""
        if self.current_date and self.editor.is_dirty():
            content = self.editor.get_content()
            if not content.strip():
                # 内容为空：不保存，但重置脏标记
                self.editor.mark_saved()
                return
            self.manager.save(self.current_date, content)
            self.editor.mark_saved()
            self.calendar_view.refresh()

    def _on_refresh(self):
        """刷新日历面板，同步文件系统实际状态"""
        self.calendar_view.refresh()
        self.status_label.setText("日历已刷新")

    def _on_delete_diary(self):
        """删除日记"""
        if self.current_date is None:
            QMessageBox.warning(self, "提示", "请先选择要删除的日记")
            return

        if not self.manager.exists(self.current_date):
            QMessageBox.warning(self, "提示", "当前日期没有日记可删除")
            return

        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除 {self.current_date.strftime('%Y-%m-%d')} 的日记吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.manager.delete(self.current_date):
                self.diary_deleted.emit(self.current_date)
                # 清空内容，但保留日期标题；标记已保存防止自动保存重建文件
                self.editor.set_content(self.current_date, "", has_diary=False)
                self.editor.mark_saved()
                self.calendar_view.refresh()
                self.status_label.setText(f"已删除: {self.current_date.strftime('%Y-%m-%d')}")
            else:
                QMessageBox.warning(self, "删除失败", "日记文件不存在或无法删除")

    def _on_content_changed(self):
        """内容变化"""
        if self.current_date:
            word_count = self.editor.get_word_count()
            self.status_label.setText(f"编辑中: {self.current_date.strftime('%Y-%m-%d')} ({word_count}字) *")

    def _on_diary_saved(self, diary_date: date):
        """日记保存后"""
        self.calendar_view.refresh()

    def _on_diary_deleted(self, diary_date: date):
        """日记删除后"""
        self.calendar_view.refresh()

    def _on_search(self):
        """搜索"""
        from PySide6.QtWidgets import QInputDialog
        keyword, ok = QInputDialog.getText(self, "搜索", "输入搜索关键词:")
        if ok and keyword:
            results = self.manager.search(keyword)
            if results:
                self._show_search_results(keyword, results)
            else:
                QMessageBox.information(self, "搜索结果", f"没有找到包含 '{keyword}' 的日记")

    def _show_search_results(self, keyword: str, results):
        """显示搜索结果"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget

        dialog = QDialog(self)
        dialog.setWindowTitle(f"搜索结果: {keyword}")
        dialog.resize(600, 400)

        layout = QVBoxLayout(dialog)

        label = QLabel(f"找到 {len(results)} 篇日记:")
        layout.addWidget(label)

        list_widget = QListWidget()
        for entry in results:
            list_widget.addItem(f"{entry.date.strftime('%Y-%m-%d')} ({entry.word_count}字)")
        list_widget.itemDoubleClicked.connect(
            lambda _, r=results, lw=list_widget: self._open_search_result(r[lw.currentRow()])
        )
        layout.addWidget(list_widget)

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)

        dialog.exec()

    def _open_search_result(self, entry):
        """打开搜索结果"""
        self.select_date(entry.date)

    def show_stats(self):
        """显示统计对话框"""
        dialog = StatsDialog(self.manager, self)
        dialog.exec()

    def closeEvent(self, event):
        """关闭事件：自动保存"""
        self._auto_save_if_needed()
        event.accept()


def main(data_dir: str = "data"):
    """启动 GUI"""
    app = QApplication([])
    window = MainWindow(data_dir=data_dir)
    window.show()
    return app.exec()
