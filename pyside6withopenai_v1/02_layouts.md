# PySide6 - Buổi 2

## Layout chuyên sâu, QLabel, QPushButton, QLineEdit

### Mục tiêu

Sau buổi này bạn sẽ:

- Hiểu Layout là gì
- Sử dụng QVBoxLayout
- Sử dụng QHBoxLayout
- Sử dụng QLabel
- Sử dụng QPushButton
- Sử dụng QLineEdit
- Xây dựng Form nhập liệu đơn giản

---

# 1. Tại sao cần Layout?

Nếu đặt widget bằng `move()`:

```text-x-trilium-auto
label.move(10, 10)
button.move(50, 100)
```

Khi phóng to hoặc thu nhỏ cửa sổ:

- Giao diện bị lệch
- Widget không tự co giãn

Qt giải quyết bằng Layout.

---

# 2. QVBoxLayout

Sắp xếp theo chiều dọc.

```text-x-trilium-auto
Label

Textbox

Button
```

Ví dụ:

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

app = QApplication(sys.argv)

window = QWidget()

layout = QVBoxLayout()

layout.addWidget(QLabel("Họ tên"))
layout.addWidget(QLineEdit())
layout.addWidget(QPushButton("Lưu"))

window.setLayout(layout)

window.show()
sys.exit(app.exec())
```

---

# 3. QHBoxLayout

Sắp xếp theo chiều ngang.

```text-x-trilium-auto
[Nút 1] [Nút 2] [Nút 3]
```

Ví dụ:

```text-x-trilium-auto
layout = QHBoxLayout()

layout.addWidget(QPushButton("Thêm"))
layout.addWidget(QPushButton("Sửa"))
layout.addWidget(QPushButton("Xóa"))
```

---

# 4. Kết hợp Layout

Đây là cách làm phổ biến nhất.

```text-x-trilium-auto
Tên

[________]

Email

[________]

[Lưu] [Thoát]
```

Code:

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

app = QApplication(sys.argv)

window = QWidget()

main_layout = QVBoxLayout()

main_layout.addWidget(QLabel("Tên"))
main_layout.addWidget(QLineEdit())

main_layout.addWidget(QLabel("Email"))
main_layout.addWidget(QLineEdit())

button_layout = QHBoxLayout()

button_layout.addWidget(QPushButton("Lưu"))
button_layout.addWidget(QPushButton("Thoát"))

main_layout.addLayout(button_layout)

window.setLayout(main_layout)

window.show()

sys.exit(app.exec())
```

---

# 5. QLabel

### Tạo Label

```text-x-trilium-auto
label = QLabel("Xin chào")
```

---

### Đổi nội dung

```text-x-trilium-auto
label.setText("Hello")
```

---

### Lấy nội dung

```text-x-trilium-auto
text = label.text()
```

---

# 6. QLineEdit

### Tạo Textbox

```text-x-trilium-auto
textbox = QLineEdit()
```

---

### Placeholder

```text-x-trilium-auto
textbox.setPlaceholderText("Nhập họ tên")
```

Kết quả:

```text-x-trilium-auto
[Nhập họ tên]
```

---

### Lấy dữ liệu

```text-x-trilium-auto
name = textbox.text()
```

---

### Xóa dữ liệu

```text-x-trilium-auto
textbox.clear()
```

---

### Mật khẩu

```text-x-trilium-auto
textbox.setEchoMode(QLineEdit.Password)
```

---

# 7. QPushButton

### Tạo Button

```text-x-trilium-auto
button = QPushButton("Lưu")
```

---

### Bắt sự kiện Click

```text-x-trilium-auto
button.clicked.connect(function_name)
```

Ví dụ:

```text-x-trilium-auto
def hello():
    print("Hello")

button.clicked.connect(hello)
```

---

# 8. Mini Project: Form Chào Hỏi

## Giao diện

```text-x-trilium-auto
Tên

[____________]

[Chào]

Xin chào ...
```

---

## Code hoàn chỉnh

```text-x-trilium-auto
import sys
from PySide6.QtWidgets import *

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buổi 2")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên")

        self.button = QPushButton("Chào")

        self.result = QLabel("")

        self.button.clicked.connect(self.say_hello)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tên"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.button)
        layout.addWidget(self.result)

        self.setLayout(layout)

    def say_hello(self):
        name = self.name_input.text()

        self.result.setText(f"Xin chào {name}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
```

---

# 9. Signal và Slot

Qt hoạt động theo cơ chế:

```text-x-trilium-auto
Signal -> Slot
```

Ví dụ:

```text-x-trilium-auto
Click nút
    ↓
clicked()
    ↓
say_hello()
```

Code:

```text-x-trilium-auto
button.clicked.connect(say_hello)
```

---

# 10. Bài tập thực hành

## Bài 1

Tạo giao diện:

```text-x-trilium-auto
Họ tên

[________]

[Nút Hiển thị]

Kết quả:
```

Khi bấm nút:

```text-x-trilium-auto
Bạn tên là Nguyễn Văn A
```

---

## Bài 2

Tạo form đăng nhập:

```text-x-trilium-auto
Tài khoản

[________]

Mật khẩu

[********]

[Đăng nhập]
```

Khi bấm:

```text-x-trilium-auto
Xin chào admin
```

---

## Bài 3

Tạo máy tính cộng đơn giản:

```text-x-trilium-auto
Số 1

[__]

Số 2

[__]

[Tính]

Kết quả: 15
```

---

# Kiến thức cần nhớ

| Widget | Chức năng |
| --- | --- |
| QWidget | Cửa sổ |
| QLabel | Hiển thị văn bản |
| QPushButton | Nút bấm |
| QLineEdit | Ô nhập liệu |
| QVBoxLayout | Xếp dọc |
| QHBoxLayout | Xếp ngang |

### Sau buổi 2

Bạn đã đủ kiến thức để làm:

- Form đăng nhập
- Form nhập dữ liệu
- Máy tính đơn giản
- App ghi chú nhỏ

👉 Gõ **"buổi 3"** để học **QMainWindow, QMessageBox, QCheckBox, QRadioButton và xây dựng ứng dụng đăng nhập chuyên nghiệp hơn**.
