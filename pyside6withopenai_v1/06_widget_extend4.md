# PySide6 - Buổi 6

# Kiến trúc dự án chuyên nghiệp - MenuBar, ToolBar, StatusBar, Action và chia nhiều file

Đây là buổi rất quan trọng. Từ hôm nay, chúng ta sẽ chuyển từ cách viết "tất cả trong một file" sang cách tổ chức dự án như các ứng dụng thực tế.

---

# Mục tiêu

Sau buổi này bạn sẽ biết:

- Tổ chức project theo chuẩn
- Chia chương trình thành nhiều file
- Sử dụng `QMenuBar`
- Sử dụng `QToolBar`
- Sử dụng `QStatusBar`
- Sử dụng `QAction`
- Sử dụng `QIcon`
- Sử dụng `QDockWidget`
- Viết ứng dụng theo hướng OOP

---

# 1. Cấu trúc dự án

Thay vì:

```text-x-trilium-auto
app.py
```

Ta sẽ tổ chức như sau:

```text-x-trilium-auto
student_manager/
│
├── main.py
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── student_form.py
│   └── student_table.py
│
├── models/
│   ├── __init__.py
│   └── student.py
│
├── services/
│   ├── __init__.py
│   └── student_service.py
│
├── resources/
│   ├── icons/
│   └── images/
│
└── data/
```

Đây là cấu trúc phổ biến trong các dự án PySide6.

---

# 2. main.py

```text-x-trilium-auto
import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())
```

`main.py` chỉ có nhiệm vụ khởi động ứng dụng.

---

# 3. MainWindow

```text-x-trilium-auto
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Student Manager")

        self.resize(1000,700)
```

Đây sẽ là cửa sổ chính.

---

# 4. QAction

`QAction` là hành động có thể dùng ở:

- Menu
- Toolbar
- Phím tắt
- Context Menu

Ví dụ:

```text-x-trilium-auto
new_action = QAction("Mới", self)
```

---

## Bắt sự kiện

```text-x-trilium-auto
new_action.triggered.connect(self.new_student)
```

---

# 5. MenuBar

Ví dụ:

```text-x-trilium-auto
File

Edit

View

Help
```

---

Tạo Menu

```text-x-trilium-auto
menu = self.menuBar()
```

---

Tạo File Menu

```text-x-trilium-auto
file_menu = menu.addMenu("&File")
```

---

Thêm Action

```text-x-trilium-auto
file_menu.addAction(new_action)
```

---

Ví dụ đầy đủ

```text-x-trilium-auto
from PySide6.QtGui import QAction

menu = self.menuBar()

file_menu = menu.addMenu("&File")

new_action = QAction("New", self)

file_menu.addAction(new_action)
```

---

# 6. Separator

```text-x-trilium-auto
file_menu.addSeparator()
```

Kết quả

```text-x-trilium-auto
New

Open

----------------

Exit
```

---

# 7. ToolBar

Toolbar giúp thao tác nhanh.

Ví dụ

```text-x-trilium-auto
🆕 💾 ✂ 📋
```

---

Tạo

```text-x-trilium-auto
toolbar = self.addToolBar("Main")
```

---

Thêm Action

```text-x-trilium-auto
toolbar.addAction(new_action)
```

---

# 8. StatusBar

Hiển thị trạng thái.

```text-x-trilium-auto
self.statusBar().showMessage("Ready")
```

---

Hiển thị trong 5 giây

```text-x-trilium-auto
self.statusBar().showMessage(
    "Đã lưu",
    5000
)
```

---

# 9. QIcon

Nếu có thư mục

```text-x-trilium-auto
resources/icons/
```

Ta dùng

```text-x-trilium-auto
from PySide6.QtGui import QIcon

icon = QIcon("resources/icons/add.png")
```

---

Áp dụng

```text-x-trilium-auto
action = QAction(icon,"Thêm",self)
```

---

# 10. Shortcut

```text-x-trilium-auto
action.setShortcut("Ctrl+N")
```

Ví dụ

```text-x-trilium-auto
Ctrl+S

Ctrl+O

Ctrl+Q
```

---

# 11. Tooltip

```text-x-trilium-auto
action.setToolTip(
    "Thêm sinh viên"
)
```

---

# 12. StatusTip

```text-x-trilium-auto
action.setStatusTip(
    "Tạo sinh viên mới"
)
```

---

# 13. QDockWidget

Dock có thể kéo thả.

Ví dụ

```text-x-trilium-auto
-------------------------

Project

Student

Teacher

Course

-------------------------

Main Area

-------------------------
```

---

Tạo

```text-x-trilium-auto
dock = QDockWidget("Danh mục")
```

---

Đặt Widget

```text-x-trilium-auto
dock.setWidget(QListWidget())
```

---

Thêm

```text-x-trilium-auto
self.addDockWidget(
    Qt.LeftDockWidgetArea,
    dock
)
```

---

# 14. Kiến trúc OOP

Không nên

```text-x-trilium-auto
class MainWindow(QMainWindow):

    def __init__(self):

        ...
```

viết toàn bộ 500 dòng trong `__init__`.

Nên chia nhỏ.

```text-x-trilium-auto
class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.create_actions()

        self.create_menu()

        self.create_toolbar()

        self.create_statusbar()

        self.create_ui()

        self.connect_signals()
```

---

Ví dụ

```text-x-trilium-auto
def create_menu(self):

    ...
```

```text-x-trilium-auto
def create_toolbar(self):

    ...
```

```text-x-trilium-auto
def connect_signals(self):

    ...
```

Code sẽ rất dễ đọc.

---

# Mini Project

## Giao diện

```text-x-trilium-auto
------------------------------------------------------

File Edit Help

------------------------------------------------------

🆕 💾 ❌

------------------------------------------------------

Student Manager

------------------------------------------------------

Ready

------------------------------------------------------
```

---

Các Action

```text-x-trilium-auto
New

Save

Exit
```

Toolbar

```text-x-trilium-auto
New

Save

Delete
```

StatusBar

```text-x-trilium-auto
Ready
```

---

# Bài tập 1

Tạo Menu

```text-x-trilium-auto
File

    New

    Open

    Save

    Exit
```

---

# Bài tập 2

Tạo Toolbar

```text-x-trilium-auto
New

Open

Save

Delete
```

---

# Bài tập 3

Khi nhấn

```text-x-trilium-auto
New
```

StatusBar đổi thành

```text-x-trilium-auto
Đang tạo sinh viên...
```

---

# Bài tập 4

Thêm Shortcut

```text-x-trilium-auto
Ctrl+N

Ctrl+S

Ctrl+Q
```

---

# Bài tập 5

Thêm DockWidget

```text-x-trilium-auto
Danh mục

Sinh viên

Giáo viên

Lớp học
```

---

# Tổng kết Buổi 6

Bạn đã học được:

| Thành phần | Vai trò |
| --- | --- |
| `QAction` | Đại diện cho một hành động có thể dùng ở nhiều nơi (menu, toolbar, phím tắt). |
| `QMenuBar` | Thanh menu chính của ứng dụng. |
| `QToolBar` | Thanh công cụ để truy cập nhanh các chức năng. |
| `QStatusBar` | Hiển thị trạng thái hoặc thông báo ngắn. |
| `QIcon` | Thêm biểu tượng cho cửa sổ và các hành động. |
| `QDockWidget` | Tạo các panel có thể kéo, thả và ẩn/hiện. |

---

# Dự án xuyên suốt khóa học

Để phù hợp với mục tiêu của bạn (xây dựng các ứng dụng desktop như trình đọc truyện, TTS và quản lý dữ liệu), từ **buổi 7** chúng ta sẽ chuyển sang một kiến trúc hoàn chỉnh theo mô hình gần giống MVC:

```text-x-trilium-auto
student_manager/
│
├── main.py
├── ui/
├── models/
├── services/
├── database/
├── resources/
└── config.py
```

Ở **buổi 7**, chúng ta sẽ tích hợp **SQLite** với PySide6:

- Tạo cơ sở dữ liệu.
- Thực hiện CRUD (Thêm, sửa, xóa, tìm kiếm).
- Hiển thị dữ liệu từ SQLite lên `QTableWidget`.
- Tách lớp truy cập dữ liệu (Repository/Service).
- Chuẩn bị nền tảng để sau này chuyển sang ORM hoặc `QSqlTableModel`. Đây là bước rất quan trọng để xây dựng các ứng dụng desktop chuyên nghiệp.
