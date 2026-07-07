# PySide6 - Buổi 3

## QMainWindow, QMessageBox, QCheckBox, QRadioButton

---

# Mục tiêu

Sau buổi học này bạn sẽ biết:

- QMainWindow là gì
- Tạo Menu Bar
- Tạo Status Bar
- Hiển thị QMessageBox
- Sử dụng QCheckBox
- Sử dụng QRadioButton
- Xây dựng Form Đăng nhập hoàn chỉnh

---

# 1. QWidget và QMainWindow

Buổi trước dùng:

```text-x-trilium-auto
window = QWidget()
```

Phù hợp với ứng dụng nhỏ.

---

Qt thường dùng:

```text-x-trilium-auto
QMainWindow
```

vì hỗ trợ:

- MenuBar
- Toolbar
- StatusBar
- DockWidget
- Central Widget

---

Ví dụ:

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

app = QApplication(sys.argv)

window = QMainWindow()

window.setWindowTitle("Main Window")
window.resize(800, 600)

window.show()

sys.exit(app.exec())
```

---

# 2. Central Widget

QMainWindow không cho đặt Layout trực tiếp.

Sai:

```text-x-trilium-auto
window.setLayout(layout)
```

Đúng:

```text-x-trilium-auto
central_widget = QWidget()

window.setCentralWidget(central_widget)

central_widget.setLayout(layout)
```

---

Ví dụ:

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

app = QApplication(sys.argv)

window = QMainWindow()

central = QWidget()

layout = QVBoxLayout()

layout.addWidget(QLabel("Xin chào"))

central.setLayout(layout)

window.setCentralWidget(central)

window.show()

sys.exit(app.exec())
```

---

# 3. QMessageBox

Dùng để hiển thị hộp thoại.

---

## Thông báo

```text-x-trilium-auto
QMessageBox.information(
    self,
    "Thông báo",
    "Lưu thành công"
)
```

---

## Cảnh báo

```text-x-trilium-auto
QMessageBox.warning(
    self,
    "Cảnh báo",
    "Chưa nhập dữ liệu"
)
```

---

## Báo lỗi

```text-x-trilium-auto
QMessageBox.critical(
    self,
    "Lỗi",
    "Đăng nhập thất bại"
)
```

---

## Hỏi xác nhận

```text-x-trilium-auto
result = QMessageBox.question(
    self,
    "Xác nhận",
    "Bạn có muốn thoát?"
)
```

---

Ví dụ:

```text-x-trilium-auto
if result == QMessageBox.Yes:
    print("Thoát")
```

---

# 4. QCheckBox

Cho phép chọn nhiều giá trị.

Ví dụ:

```text-x-trilium-auto
☑ Python
☑ Dart
☐ Golang
```

---

Code:

```text-x-trilium-auto
checkbox = QCheckBox("Python")
```

---

Kiểm tra trạng thái:

```text-x-trilium-auto
checkbox.isChecked()
```

---

Ví dụ:

```text-x-trilium-auto
if checkbox.isChecked():
    print("Đã chọn")
```

---

# 5. QRadioButton

Chỉ được chọn 1 trong nhiều lựa chọn.

---

Ví dụ:

```text-x-trilium-auto
(*) Nam
( ) Nữ
```

---

Code:

```text-x-trilium-auto
male = QRadioButton("Nam")
female = QRadioButton("Nữ")
```

---

Kiểm tra:

```text-x-trilium-auto
male.isChecked()
```

---

# 6. Mini Project: Khảo sát giới tính

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.male = QRadioButton("Nam")
        self.female = QRadioButton("Nữ")

        self.button = QPushButton("Xác nhận")

        self.button.clicked.connect(self.show_gender)

        layout = QVBoxLayout()

        layout.addWidget(self.male)
        layout.addWidget(self.female)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def show_gender(self):

        if self.male.isChecked():
            QMessageBox.information(
                self,
                "Thông báo",
                "Bạn chọn Nam"
            )

        elif self.female.isChecked():
            QMessageBox.information(
                self,
                "Thông báo",
                "Bạn chọn Nữ"
            )

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
```

---

# 7. Menu Bar

Ví dụ:

```text-x-trilium-auto
menu_bar = self.menuBar()
```

---

Tạo menu:

```text-x-trilium-auto
file_menu = menu_bar.addMenu("File")
```

---

Tạo Action:

```text-x-trilium-auto
exit_action = QAction("Thoát", self)
```

---

Gắn vào menu:

```text-x-trilium-auto
file_menu.addAction(exit_action)
```

---

Bắt sự kiện:

```text-x-trilium-auto
exit_action.triggered.connect(self.close)
```

---

# 8. Status Bar

```text-x-trilium-auto
self.statusBar().showMessage(
    "Sẵn sàng"
)
```

---

Ví dụ:

```text-x-trilium-auto
self.statusBar().showMessage(
    "Đăng nhập thành công"
)
```

---

# 9. Dự án: Form Đăng Nhập Chuyên Nghiệp

## Giao diện

```text-x-trilium-auto
Tài khoản

[________]

Mật khẩu

[********]

☑ Ghi nhớ đăng nhập

[Đăng nhập]
```

---

## Code hoàn chỉnh

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Đăng nhập")

        central = QWidget()

        self.setCentralWidget(central)

        self.username = QLineEdit()

        self.password = QLineEdit()
        self.password.setEchoMode(
            QLineEdit.Password
        )

        self.remember = QCheckBox(
            "Ghi nhớ đăng nhập"
        )

        self.login_button = QPushButton(
            "Đăng nhập"
        )

        self.login_button.clicked.connect(
            self.login
        )

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tài khoản"))
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Mật khẩu"))
        layout.addWidget(self.password)

        layout.addWidget(self.remember)

        layout.addWidget(self.login_button)

        central.setLayout(layout)

    def login(self):

        user = self.username.text()
        password = self.password.text()

        if user == "admin" and password == "123":

            QMessageBox.information(
                self,
                "Thành công",
                "Đăng nhập thành công"
            )

        else:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Sai tài khoản hoặc mật khẩu"
            )

app = QApplication(sys.argv)

window = LoginWindow()
window.show()

sys.exit(app.exec())
```

---

# Bài tập

## Bài 1

Tạo khảo sát:

```text-x-trilium-auto
Bạn thích ngôn ngữ nào?

☑ Python
☑ Dart
☑ Go

[Xác nhận]
```

Hiển thị các lựa chọn đã chọn.

---

## Bài 2

Tạo Form:

```text-x-trilium-auto
Họ tên

[________]

Giới tính

(*) Nam
( ) Nữ

[Xác nhận]
```

Hiển thị kết quả bằng QMessageBox.

---

## Bài 3

Nâng cấp Form đăng nhập:

- Sai quá 3 lần thì khóa nút đăng nhập.
- Hiển thị số lần đăng nhập sai trong StatusBar.

---

# Kiến thức hôm nay

| Thành phần | Công dụng |
| --- | --- |
| QMainWindow | Cửa sổ chính |
| QWidget | Widget cơ sở |
| QMessageBox | Hộp thoại |
| QCheckBox | Chọn nhiều |
| QRadioButton | Chọn một |
| MenuBar | Thanh menu |
| StatusBar | Thanh trạng thái |

👉 Gõ **"buổi 4"** để học **QComboBox, QListWidget, QTextEdit, QSpinBox và xây dựng ứng dụng Quản lý công việc (Todo App)**.
