# 📖 日记本应用

一个简洁、高效的日记管理工具，支持命令行和图形界面。

## 功能特性

- ✅ **增删改查**：完整的日记 CRUD 操作
- 📅 **日历视图**：直观查看哪天写了、哪天没写
- 📊 **统计分析**：统计每天字数、写了多少天
- 🔍 **全文搜索**：快速找到包含关键词的日记
- 📁 **数据分离**：纯文本存储，随时备份，安全可靠
- 🔄 **自动导入**：启动时自动识别 data 目录下的历史日记

## 目录结构

```
Diary_manager/
├── data/                    # 日记数据存储
│   └── 2026/
│       ├── 20260101.txt
│       └── 20260102.txt
│
├── core/                    # 核心业务逻辑（与UI分离）
│   ├── models.py            # 数据模型
│   ├── storage.py           # 文件存储
│   ├── diary_manager.py     # 日记管理
│   └── calendar_service.py  # 日历服务
│
├── cli/                     # 命令行接口
│   └── cli.py
│
├── gui/                     # 图形界面 (PySide6)
│   ├── main_window.py       # 主窗口
│   ├── calendar_view.py      # 日历视图
│   ├── diary_editor.py       # 日记编辑器
│   └── stats_dialog.py      # 统计对话框
│
├── utils/                    # 工具函数
│   └── date_utils.py
│
├── main.py                   # 入口文件
└── README.md
```

## 安装依赖

```bash
pip install PySide6
```

## 使用方法

### 图形界面

```bash
python main.py --gui
# 或简写
python main.py -g
```

### 命令行

```bash
# 新建日记
python main.py new 2026-05-20 --content "今天是个好日子"

# 保存日记（覆盖）
python main.py save 2026-05-20 --content "更新内容"

# 查看日记
python main.py view 2026-05-20

# 删除日记
python main.py delete 2026-05-20

# 列出日记
python main.py list 2026        # 列出2026年
python main.py list all         # 列出所有

# 搜索
python main.py search "关键词"

# 统计
python main.py stats            # 全局统计
python main.py stats 2026       # 2026年统计

# 日历
python main.py calendar          # 本月日历
python main.py calendar 2026 5   # 2026年5月

# 导入
python main.py import /path/to/dir    # 从目录导入
python main.py auto-import            # 自动导入 data 目录
```

### 交互模式

```bash
python main.py
# 进入交互式命令行
diary> list 2026
diary> view 2026-01-01
diary> search "学习"
diary> quit
```

## 数据格式

- 存储位置：`data/年份/YYYYMMDD.txt`
- 编码：`UTF-8`
- 格式：纯文本

## 数据备份

数据完全以文本文件存储，可以：
1. 直接复制 `data/` 目录进行备份
2. 使用任意文本编辑器打开和编辑
3. 用 git 等工具进行版本控制

## 历史数据导入

### 方式一：自动导入（推荐）

启动 GUI 时，程序会自动扫描 `data/` 目录，将散落在各处的日记文件自动归类到正确的年份目录。

### 方式二：手动导入

```bash
python main.py import /path/to/old_diaries
```

### 方式三：直接放置

将符合格式的日记文件（`YYYYMMDD.txt` 或 `YYYYMMDD.md`）直接放到 `data/` 目录，下次启动时会自动识别。

## GUI 快捷键

- `Ctrl+S` - 保存
- `Ctrl+N` - 新建今天日记
- `Ctrl++` - 增大字体
- `Ctrl+-` - 减小字体
- `Ctrl+F` - 搜索
