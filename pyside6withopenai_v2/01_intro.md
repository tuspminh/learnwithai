# Khóa học PySide6 từ A-Z

# Buổi 1: Làm quen với PySide6 và tạo ứng dụng GUI đầu tiên

Mục tiêu của buổi học:

Sau buổi này bạn sẽ hiểu:

- GUI là gì?
- Qt là gì?
- PySide6 là gì?
- Cách cài đặt môi trường
- Kiến trúc của một ứng dụng Qt
- QApplication hoạt động như thế nào
- QWidget là gì
- QLabel
- QPushButton
- Layout cơ bản
- Signal và Slot (giới thiệu)
- Viết ứng dụng đầu tiên đúng chuẩn

Đến cuối buổi, chúng ta sẽ xây dựng một cửa sổ có tiêu đề, văn bản, nút bấm và xử lý sự kiện.

---

# 1. GUI là gì?

GUI (Graphical User Interface) là giao diện đồ họa giúp người dùng tương tác với chương trình bằng:

- Cửa sổ
- Nút bấm
- Ô nhập liệu
- Danh sách
- Menu
- Hình ảnh

Ví dụ:

```text-x-trilium-auto
+---------------------------------------+
| Demo PySide6                          |
+---------------------------------------+

Xin chào!

[Tên của bạn____________]

        [ Xin chào ]
```

Khác với chương trình Console:

```text-x-trilium-auto
Nhập tên:
>
```

GUI thân thiện và chuyên nghiệp hơn rất nhiều.

---

# 2. Qt là gì?

Qt là framework GUI nổi tiếng của C++.

Nó được dùng để viết:

- Adobe Photoshop Launcher
- Autodesk Maya
- VLC
- Telegram Desktop
- Wireshark
- VirtualBox
- Qt Creator
- Nhiều phần mềm công nghiệp và y tế

Qt hỗ trợ:

- Windows
- Linux
- macOS
- Android
- iOS
- Embedded Linux

Một lần viết, chạy trên nhiều hệ điều hành.

---

# 3. PySide6 là gì?

PySide6 là binding chính thức của Qt 6 dành cho Python.

Có thể hiểu:

```text-x-trilium-auto
Qt (C++)
      │
      │ Binding
      ▼
PySide6 (Python)
```

Ta được sử dụng toàn bộ sức mạnh của Qt bằng Python.

---

# 4. PySide6 và PyQt khác nhau thế nào?

| PySide6 | PyQt6 |
| --- | --- |
| Chính thức từ Qt | Bên thứ ba |
| License LGPL | GPL hoặc thương mại |
| API gần như giống nhau | API gần như giống nhau |
| Khuyến nghị cho dự án mới | Cũng rất phổ biến |

Trong khóa học này chúng ta sử dụng **PySide6**.

---

# 5. Cài đặt

Tạo môi trường ảo:

```text-x-trilium-auto
python -m venv .venv
```

Kích hoạt:

### Windows

```text-x-trilium-auto
.venv\Scripts\activate
```

### Linux/macOS

```text-x-trilium-auto
source .venv/bin/activate
```

Cài PySide6:

```text-x-trilium-auto
pip install pyside6
```

Kiểm tra:

```text-x-trilium-auto
python -c "import PySide6; print(PySide6.__version__)"
```

Nếu in ra phiên bản là cài đặt thành công.

---

# 6. Cấu trúc một ứng dụng Qt

Ứng dụng Qt luôn có các thành phần chính:

```text-x-trilium-auto
app.py

↓

QApplication

↓

Window (QWidget)

↓

Layout

↓

Widgets
```

Ví dụ:

```text-x-trilium-auto
Application
      │
      ▼
 MainWindow
      │
 ┌────┴────────┐
 │             │
Button      Label
```

---

# 7. QApplication là gì?

Đây là đối tượng **quan trọng nhất** của mọi ứng dụng Qt.

Nó quản lý:

- toàn bộ cửa sổ
- chuột
- bàn phím
- theme
- sự kiện
- vòng lặp sự kiện (event loop)

Nếu không có QApplication thì giao diện sẽ không thể hoạt động.

Ví dụ tối thiểu:

```text-x-trilium-auto
import sys

from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)

app.exec()
```

Ở đây chưa có cửa sổ nên chương trình chạy nhưng không hiển thị gì.

---

# 8. QWidget là gì?

`QWidget` là lớp cơ sở của hầu hết các thành phần giao diện.

Mọi thứ bạn nhìn thấy trên màn hình đều kế thừa từ `QWidget`.

Ví dụ:

```text-x-trilium-auto
QWidget
   │
   ├── QLabel
   ├── QPushButton
   ├── QTextEdit
   ├── QListWidget
   ├── QTableWidget
   └── ...
```

Một cửa sổ đơn giản:

```text-x-trilium-auto
import sys

from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()

window.show()

app.exec()
```

Kết quả:

```text-x-trilium-auto
+---------------------+

       Cửa sổ trắng

+---------------------+
```

---

# 9. Đặt tiêu đề

```text-x-trilium-auto
window.setWindowTitle("Buổi 1 - PySide6")
```

---

# 10. Đặt kích thước

```text-x-trilium-auto
window.resize(800, 600)
```

hoặc

```text-x-trilium-auto
window.setFixedSize(800, 600)
```

Khác nhau:

```text-x-trilium-auto
resize()

→ người dùng vẫn thay đổi được kích thước

setFixedSize()

→ khóa kích thước
```

---

# 11. QLabel

Hiển thị văn bản.

```text-x-trilium-auto
from PySide6.QtWidgets import QLabel

label = QLabel("Xin chào PySide6")
```

Nhưng nếu chỉ tạo `QLabel`, nó chưa được hiển thị. Ta cần thêm nó vào một `layout` hoặc gán cha (`parent`) để nó xuất hiện trong cửa sổ.

---

# 12. QPushButton

```text-x-trilium-auto
button = QPushButton("Nhấn tôi")
```

Khi bấm sẽ phát ra signal:

```text-x-trilium-auto
clicked
```

Buổi sau chúng ta sẽ học kỹ về Signal và Slot.

---

# 13. Layout

Đây là khái niệm **rất quan trọng**.

Nếu không có Layout, bạn sẽ phải tự tính tọa độ:

```text-x-trilium-auto
x = 15

y = 23
```

Điều này rất khó bảo trì.

Qt khuyến khích dùng Layout.

Ví dụ `QVBoxLayout`:

```text-x-trilium-auto
+----------------+

Label

Button

Button

Button

+----------------+
```

Các widget sẽ tự sắp xếp theo chiều dọc.

---

# 14. Ví dụ hoàn chỉnh đầu tiên

```text-x-trilium-auto
import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def on_button_clicked():
    print("Bạn vừa nhấn nút!")


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("PySide6 - Buổi 1")
window.resize(400, 200)

layout = QVBoxLayout()

label = QLabel("Chào mừng bạn đến với PySide6!")
button = QPushButton("Nhấn tôi")

button.clicked.connect(on_button_clicked)

layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)

window.show()

app.exec()
```

### Giải thích từng bước

```text-x-trilium-auto
app = QApplication(sys.argv)
```

Tạo ứng dụng.

```text-x-trilium-auto
window = QWidget()
```

Tạo cửa sổ.

```text-x-trilium-auto
layout = QVBoxLayout()
```

Tạo bố cục theo chiều dọc.

```text-x-trilium-auto
layout.addWidget(label)
```

Đưa `label` vào bố cục.

```text-x-trilium-auto
window.setLayout(layout)
```

Gắn bố cục cho cửa sổ.

```text-x-trilium-auto
window.show()
```

Hiển thị cửa sổ.

```text-x-trilium-auto
app.exec()
```

Bắt đầu vòng lặp sự kiện (event loop). Từ thời điểm này, ứng dụng sẽ chờ và xử lý các thao tác như nhấn nút, nhập liệu, kéo cửa sổ,...

---

# 15. Signal và Slot (giới thiệu)

Qt sử dụng cơ chế Signal và Slot để các đối tượng giao tiếp với nhau.

```text-x-trilium-auto
Button

↓

clicked Signal

↓

Slot

↓

Hàm Python
```

Ví dụ:

```text-x-trilium-auto
button.clicked.connect(on_button_clicked)
```

Khi người dùng nhấn nút:

```text-x-trilium-auto
clicked()

↓

connect()

↓

on_button_clicked()

↓

print(...)
```

Đây là nền tảng của lập trình giao diện trong Qt.

---

# 16. Những lỗi người mới thường gặp

### Quên gọi `show()`

```text-x-trilium-auto
window.show()
```

Nếu quên, cửa sổ sẽ không xuất hiện.

---

### Quên `app.exec()`

```text-x-trilium-auto
app.exec()
```

Chương trình sẽ kết thúc ngay lập tức.

---

### Không gắn Layout

```text-x-trilium-auto
window.setLayout(layout)
```

Nếu quên, các widget sẽ không được bố trí và giao diện sẽ không hiển thị như mong muốn.

---

### Tạo widget nhưng không thêm vào Layout

Sai:

```text-x-trilium-auto
button = QPushButton("OK")
```

Đúng:

```text-x-trilium-auto
layout.addWidget(button)
```

---

# 17. Bài tập thực hành

## Bài 1

Tạo cửa sổ:

- tiêu đề "Thông tin cá nhân"
- kích thước 500 × 300

---

## Bài 2

Hiển thị:

```text-x-trilium-auto
Họ tên

Lớp

Trường
```

Mỗi dòng là một `QLabel`.

---

## Bài 3

Thêm 2 nút:

```text-x-trilium-auto
Lưu

Thoát
```

---

## Bài 4

Khi nhấn nút "Lưu"

In ra:

```text-x-trilium-auto
Đã lưu dữ liệu!
```

---

## Bài 5

Khi nhấn nút "Thoát"

Đóng chương trình.

*Gợi ý:*

```text-x-trilium-auto
button_exit.clicked.connect(window.close)
```

---

# Mini Project cuối buổi

Hãy xây dựng ứng dụng **"Xin chào PySide6"** với các yêu cầu:

- Cửa sổ tiêu đề "Xin chào PySide6".
- Một `QLabel` hiển thị dòng chữ chào mừng.
- Hai `QPushButton`: **Chào** và **Thoát**.
- Khi nhấn **Chào**, in ra `"Xin chào từ PySide6!"` trên terminal.
- Khi nhấn **Thoát**, đóng cửa sổ.

---

## Tổng kết Buổi 1

Bạn đã nắm được những khái niệm nền tảng nhất của PySide6:

- Hiểu vai trò của Qt và PySide6.
- Biết cách tạo một ứng dụng Qt với `QApplication`.
- Tạo cửa sổ bằng `QWidget`.
- Thiết lập tiêu đề và kích thước cửa sổ.
- Sử dụng `QLabel`, `QPushButton`.
- Sắp xếp giao diện bằng `QVBoxLayout`.
- Kết nối sự kiện thông qua `Signal` và `Slot`.
- Hiểu vòng lặp sự kiện (`app.exec()`).

Ở **Buổi 2**, chúng ta sẽ đi sâu vào **Layout** (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`, `QFormLayout`), học cách thiết kế giao diện linh hoạt, co giãn theo kích thước cửa sổ và xây dựng các biểu mẫu (form) chuyên nghiệp. Đây là nền tảng để tạo những giao diện thực tế như phần mềm quản lý, ứng dụng học tập hay công cụ làm việc.
