# PySide6 - Buổi 4

# QComboBox, QListWidget, QTextEdit, QSpinBox và Todo App

Đến buổi này, bạn sẽ bắt đầu làm quen với các widget thường dùng trong các ứng dụng quản lý dữ liệu.

---

# Mục tiêu

Sau buổi học này, bạn sẽ biết cách sử dụng:

- `QComboBox`
- `QListWidget`
- `QTextEdit`
- `QSpinBox`
- `QGroupBox`
- Tổ chức giao diện bằng nhiều Layout
- Xây dựng ứng dụng Todo đơn giản

---

# 1. QComboBox

QComboBox là hộp chọn (dropdown).

Ví dụ:

```text-x-trilium-auto
Chọn ngôn ngữ

▼ Python
  Dart
  Go
  Rust
```

---

## Thêm dữ liệu

```text-x-trilium-auto
combo = QComboBox()

combo.addItem("Python")
combo.addItem("Dart")
combo.addItem("Go")
```

Hoặc:

```text-x-trilium-auto
combo.addItems([
    "Python",
    "Dart",
    "Go",
    "Rust"
])
```

---

## Lấy giá trị

```text-x-trilium-auto
text = combo.currentText()

print(text)
```

---

## Lấy chỉ số

```text-x-trilium-auto
index = combo.currentIndex()
```

---

## Chọn phần tử theo chỉ số

```text-x-trilium-auto
combo.setCurrentIndex(2)
```

---

## Xử lý khi thay đổi

```text-x-trilium-auto
combo.currentTextChanged.connect(self.changed)
```

Ví dụ:

```text-x-trilium-auto
def changed(self, text):
    print(text)
```

---

# 2. QListWidget

Dùng để hiển thị danh sách.

```text-x-trilium-auto
Python

Dart

Rust

Go
```

---

## Tạo

```text-x-trilium-auto
list_widget = QListWidget()
```

---

## Thêm phần tử

```text-x-trilium-auto
list_widget.addItem("Python")
```

Hoặc:

```text-x-trilium-auto
list_widget.addItems([
    "Python",
    "Dart",
    "Go"
])
```

---

## Lấy phần tử đang chọn

```text-x-trilium-auto
item = list_widget.currentItem()

if item:
    print(item.text())
```

---

## Xóa phần tử

```text-x-trilium-auto
row = list_widget.currentRow()

list_widget.takeItem(row)
```

---

## Đếm số phần tử

```text-x-trilium-auto
count = list_widget.count()
```

---

## Xóa toàn bộ

```text-x-trilium-auto
list_widget.clear()
```

---

# 3. QTextEdit

Cho phép nhập nhiều dòng văn bản.

```text-x-trilium-auto
Nội dung

Lorem ipsum...
Lorem ipsum...
Lorem ipsum...
```

---

## Tạo

```text-x-trilium-auto
editor = QTextEdit()
```

---

## Đặt nội dung

```text-x-trilium-auto
editor.setPlainText("Xin chào")
```

---

## Lấy nội dung

```text-x-trilium-auto
text = editor.toPlainText()
```

---

## Xóa

```text-x-trilium-auto
editor.clear()
```

---

## Placeholder

```text-x-trilium-auto
editor.setPlaceholderText(
    "Nhập ghi chú..."
)
```

---

# 4. QSpinBox

Nhập số bằng nút tăng giảm.

```text-x-trilium-auto
Tuổi

[25 ▲▼]
```

---

## Tạo

```text-x-trilium-auto
spin = QSpinBox()
```

---

## Giới hạn

```text-x-trilium-auto
spin.setRange(1, 100)
```

---

## Giá trị mặc định

```text-x-trilium-auto
spin.setValue(20)
```

---

## Lấy giá trị

```text-x-trilium-auto
age = spin.value()
```

---

# 5. QGroupBox

Nhóm các widget liên quan.

```text-x-trilium-auto
-------------------------
Thông tin

Tên

Email
-------------------------
```

Ví dụ:

```text-x-trilium-auto
group = QGroupBox("Thông tin")
```

---

# 6. Mini Project 1: Quản lý ngôn ngữ lập trình

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.combo = QComboBox()

        self.combo.addItems([
            "Python",
            "Dart",
            "Go",
            "Rust"
        ])

        self.button = QPushButton("Thêm")

        self.list = QListWidget()

        self.button.clicked.connect(self.add_language)

        layout = QVBoxLayout()

        layout.addWidget(self.combo)
        layout.addWidget(self.button)
        layout.addWidget(self.list)

        self.setLayout(layout)

    def add_language(self):

        self.list.addItem(
            self.combo.currentText()
        )

app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())
```

---

# 7. Mini Project 2: Ghi chú

```text-x-trilium-auto
Tiêu đề

[________]

Nội dung

[ QTextEdit ]

[Lưu]
```

Ý tưởng:

- Tiêu đề → `QLineEdit`
- Nội dung → `QTextEdit`
- Nút Lưu → `QPushButton`
- Hiển thị thông báo bằng `QMessageBox`

---

# 8. Dự án Buổi 4: Todo App

## Giao diện

```text-x-trilium-auto
──────────────────────────

Tên công việc

[_______________]

Mức ưu tiên

▼ Cao

Mô tả

┌────────────────────┐
│                    │
│ QTextEdit          │
│                    │
└────────────────────┘

[Thêm]

──────────────────────────

Danh sách

• Học Python

• Học PySide6

• Làm bài tập

──────────────────────────

[Xóa]

──────────────────────────
```

---

## Code hoàn chỉnh

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

class Todo(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Todo App")

        self.task = QLineEdit()

        self.priority = QComboBox()

        self.priority.addItems([
            "Cao",
            "Trung bình",
            "Thấp"
        ])

        self.note = QTextEdit()

        self.list = QListWidget()

        self.add_button = QPushButton("Thêm")

        self.delete_button = QPushButton("Xóa")

        self.add_button.clicked.connect(self.add_task)

        self.delete_button.clicked.connect(self.delete_task)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tên công việc"))

        layout.addWidget(self.task)

        layout.addWidget(QLabel("Ưu tiên"))

        layout.addWidget(self.priority)

        layout.addWidget(QLabel("Mô tả"))

        layout.addWidget(self.note)

        layout.addWidget(self.add_button)

        layout.addWidget(self.list)

        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def add_task(self):

        name = self.task.text()

        if name == "":

            QMessageBox.warning(
                self,
                "Lỗi",
                "Chưa nhập công việc"
            )

            return

        text = f"[{self.priority.currentText()}] {name}"

        self.list.addItem(text)

        self.task.clear()

        self.note.clear()

    def delete_task(self):

        row = self.list.currentRow()

        if row >= 0:

            self.list.takeItem(row)

app = QApplication(sys.argv)

window = Todo()

window.show()

sys.exit(app.exec())
```

---

# Bài tập

### Bài 1

Tạo ứng dụng **Quản lý sách**.

Thông tin mỗi sách:

- Tên sách (`QLineEdit`)
- Thể loại (`QComboBox`)
- Mô tả (`QTextEdit`)
- Danh sách (`QListWidget`)

Chức năng:

- Thêm
- Xóa

---

### Bài 2

Tạo ứng dụng **Danh sách mua sắm**.

Ví dụ:

```text-x-trilium-auto
Sữa

Bánh mì

Trứng

Coca
```

Có nút:

- Thêm
- Xóa
- Xóa tất cả

---

### Bài 3

Nâng cấp Todo App:

- Thêm nút **Sửa**.
- Hiển thị số lượng công việc bằng `QLabel`.
- Khi nhấp đúp vào một công việc, hiển thị mô tả bằng `QMessageBox`.
- Lưu cả **tên**, **mức ưu tiên** và **mô tả** bằng `QListWidgetItem` và `setData()` thay vì chỉ ghép thành chuỗi.

---

# Tổng kết Buổi 4

Bạn đã học được:

| Widget | Công dụng |
| --- | --- |
| `QComboBox` | Hộp chọn (dropdown) |
| `QListWidget` | Danh sách |
| `QTextEdit` | Nhập văn bản nhiều dòng |
| `QSpinBox` | Nhập số |
| `QGroupBox` | Nhóm các widget |

## Lưu ý về thực hành

Trong các buổi tiếp theo, chúng ta sẽ dần chuyển sang phong cách lập trình chuyên nghiệp hơn:

- Tách giao diện (UI) và xử lý (logic).
- Sử dụng `QMainWindow` làm cửa sổ chính.
- Tổ chức mã theo lớp và nhiều tệp.
- Chuẩn bị để dùng **Qt Designer**, **SQLite**, **Model/View**, và xây dựng các ứng dụng quy mô lớn.

Đây cũng là phong cách được sử dụng trong các dự án PySide6 thực tế.

👉 Ở **buổi 5**, chúng ta sẽ học **QTableWidget, QTabWidget, QSplitter, QFrame, QDateEdit, QFileDialog** và xây dựng một ứng dụng **Quản lý sinh viên** với giao diện nhiều tab và bảng dữ liệu.
