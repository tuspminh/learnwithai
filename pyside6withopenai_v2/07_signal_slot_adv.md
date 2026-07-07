# Khóa học PySide6 từ A-Z

# Buổi 7: Signal & Slot nâng cao - Lambda, Partial, Custom Signal và giao tiếp giữa các cửa sổ

> **Mục tiêu của buổi học**
> 
> Sau buổi này bạn sẽ:
> 
> - Thành thạo `lambda` trong `connect()`.
> - Biết sử dụng `functools.partial`.
> - Tự tạo Signal bằng `Signal`.
> - Tự tạo Slot bằng `@Slot`.
> - Truyền dữ liệu giữa các cửa sổ.
> - Hiểu kiến trúc Event-Driven chuyên nghiệp.
> - Xây dựng ứng dụng nhiều cửa sổ.

---

# 1. Ôn tập

Buổi trước chúng ta đã học:

```text-x-trilium-auto
button.clicked.connect(hello)
```

Qt sẽ thực hiện:

```text-x-trilium-auto
Người dùng

↓

Nhấn Button

↓

clicked Signal

↓

hello()
```

Nhưng nếu muốn truyền thêm dữ liệu thì sao?

Ví dụ:

```text-x-trilium-auto
save(15)
```

Không thể viết:

```text-x-trilium-auto
button.clicked.connect(save(15))
```

Vì:

- `save(15)` sẽ chạy ngay khi chương trình khởi động.
- `connect()` sẽ không còn nhận được hàm để gọi khi nhấn nút.

Đây là lúc chúng ta cần `lambda`.

---

# 2. Lambda

Ví dụ:

```text-x-trilium-auto
button.clicked.connect(
    lambda: save(15)
)
```

Trong đó:

```text-x-trilium-auto
def save(id):
    print(id)
```

Khi nhấn nút:

```text-x-trilium-auto
15
```

---

## Vì sao dùng lambda?

Ví dụ:

```text-x-trilium-auto
button.clicked.connect(
    lambda: print("Python")
)
```

Khi chưa nhấn nút:

**Không có gì xảy ra.**

Khi nhấn:

```text-x-trilium-auto
Python
```

`lambda` tạo ra một hàm ẩn danh (anonymous function) được gọi đúng thời điểm Signal phát ra.

---

# 3. Lambda với nhiều tham số

```text-x-trilium-auto
def login(username, password):
    print(username)
    print(password)
```

```text-x-trilium-auto
button.clicked.connect(
    lambda: login(
        "admin",
        "123456"
    )
)
```

Kết quả:

```text-x-trilium-auto
admin

123456
```

---

# 4. Lambda lấy dữ liệu từ Widget

Ví dụ:

```text-x-trilium-auto
button.clicked.connect(
    lambda: print(name_edit.text())
)
```

Mỗi lần nhấn nút:

Qt sẽ đọc dữ liệu **hiện tại** trong `QLineEdit`.

---

# 5. Ví dụ thực tế

```text-x-trilium-auto
from PySide6.QtWidgets import *

app = QApplication([])

window = QWidget()

layout = QVBoxLayout()

edit = QLineEdit()

button = QPushButton("Hiển thị")

layout.addWidget(edit)
layout.addWidget(button)

window.setLayout(layout)

button.clicked.connect(
    lambda: print(edit.text())
)

window.show()

app.exec()
```

Nếu nhập:

```text-x-trilium-auto
Python
```

Terminal:

```text-x-trilium-auto
Python
```

---

# 6. functools.partial

Ngoài `lambda`, Python còn có:

```text-x-trilium-auto
from functools import partial
```

Ví dụ:

```text-x-trilium-auto
from functools import partial

button.clicked.connect(
    partial(save, 15)
)
```

Kết quả:

```text-x-trilium-auto
15
```

---

## Khi nào dùng `partial`?

- Có nhiều tham số cố định.
- Muốn tái sử dụng hàm.
- Giúp mã nguồn dễ đọc hơn trong các dự án lớn.

---

# 7. Lambda hay Partial?

| Lambda | Partial |
| --- | --- |
| Linh hoạt | Gọn gàng |
| Dễ viết | Dễ tái sử dụng |
| Phù hợp xử lý nhanh | Phù hợp dự án lớn |

Cả hai đều rất phổ biến trong PySide6.

---

# 8. Custom Signal

Đây là một trong những sức mạnh lớn nhất của Qt.

Bạn có thể **tự tạo Signal**.

Ví dụ:

```text-x-trilium-auto
from PySide6.QtCore import QObject, Signal

class Worker(QObject):

    finished = Signal()
```

Ở đây:

```text-x-trilium-auto
Worker

↓

finished

↓

Signal mới
```

Signal này không có sẵn trong Qt, do chính bạn định nghĩa.

---

# 9. Signal có dữ liệu

Ví dụ:

```text-x-trilium-auto
class Worker(QObject):

    progress = Signal(int)
```

Signal sẽ gửi:

```text-x-trilium-auto
0

↓

10

↓

50

↓

100
```

Đây là cách rất phổ biến để cập nhật thanh tiến trình (`QProgressBar`) từ luồng nền.

---

# 10. Emit Signal

Để phát Signal:

```text-x-trilium-auto
self.progress.emit(50)
```

Qt sẽ gửi giá trị `50` đến tất cả Slot đã kết nối.

---

# 11. Nhận Signal

```text-x-trilium-auto
worker.progress.connect(update_progress)
```

```text-x-trilium-auto
def update_progress(value):
    print(value)
```

Kết quả:

```text-x-trilium-auto
50
```

---

# 12. Signal có nhiều tham số

```text-x-trilium-auto
class Worker(QObject):

    done = Signal(str, int)
```

Emit:

```text-x-trilium-auto
self.done.emit(
    "Python",

    100
)
```

Slot:

```text-x-trilium-auto
def finished(name, percent):
    print(name)

    print(percent)
```

Kết quả:

```text-x-trilium-auto
Python

100
```

---

# 13. @Slot

Qt cũng cho phép đánh dấu hàm là Slot.

Ví dụ:

```text-x-trilium-auto
from PySide6.QtCore import Slot
```

```text-x-trilium-auto
@Slot()
def hello():
    print("Xin chào")
```

Hoặc:

```text-x-trilium-auto
@Slot(int)
def update(value):
    print(value)
```

### Lợi ích

- Mã rõ ràng hơn.
- Qt tối ưu hiệu năng.
- Kiểm tra kiểu tham số tốt hơn.
- Đặc biệt hữu ích khi làm việc với `QThread`.

---

# 14. Giao tiếp giữa hai cửa sổ

Giả sử có:

```text-x-trilium-auto
MainWindow

↓

Mở

↓

Dialog
```

Khi người dùng nhập tên trong Dialog và nhấn **OK**, MainWindow cần nhận được tên đó.

Đây là tình huống rất phổ biến.

---

## Cách làm chuyên nghiệp

Dialog phát Signal:

```text-x-trilium-auto
class NameDialog(QDialog):

    accepted_name = Signal(str)
```

Người dùng nhấn OK:

```text-x-trilium-auto
self.accepted_name.emit(name)
```

MainWindow:

```text-x-trilium-auto
dialog.accepted_name.connect(
    self.receive_name
)
```

Slot:

```text-x-trilium-auto
def receive_name(name):
    print(name)
```

Luồng hoạt động:

```text-x-trilium-auto
Dialog

↓

Signal

↓

MainWindow

↓

Cập nhật Label
```

Đây là cách giao tiếp được khuyến nghị, thay vì để cửa sổ con truy cập trực tiếp vào cửa sổ cha.

---

# 15. Ví dụ hoàn chỉnh: Nhiều nút dùng chung một hàm

```text-x-trilium-auto
import sys

from functools import partial

from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def show_color(color):
    print(color)


app = QApplication(sys.argv)

window = QWidget()

layout = QVBoxLayout()

for color in ["Đỏ", "Xanh", "Vàng"]:

    button = QPushButton(color)

    button.clicked.connect(
        partial(show_color, color)
    )

    layout.addWidget(button)

window.setLayout(layout)

window.show()

app.exec()
```

Khi nhấn:

```text-x-trilium-auto
Đỏ
```

Terminal:

```text-x-trilium-auto
Đỏ
```

---

# 16. Ví dụ: Custom Signal

```text-x-trilium-auto
from PySide6.QtCore import QObject, Signal


class Counter(QObject):

    changed = Signal(int)

    def increase(self, value):
        self.changed.emit(value)


counter = Counter()


def show(value):
    print(value)


counter.changed.connect(show)

counter.increase(10)
```

Kết quả:

```text-x-trilium-auto
10
```

---

# 17. Những lỗi người mới thường gặp

## Lỗi 1

```text-x-trilium-auto
button.clicked.connect(
    save(5)
)
```

Sai.

Đúng:

```text-x-trilium-auto
button.clicked.connect(
    lambda: save(5)
)
```

Hoặc:

```text-x-trilium-auto
button.clicked.connect(
    partial(save, 5)
)
```

---

## Lỗi 2

Quên `emit()`.

Sai:

```text-x-trilium-auto
self.finished
```

Đúng:

```text-x-trilium-auto
self.finished.emit()
```

Chỉ tham chiếu Signal sẽ không phát sự kiện.

---

## Lỗi 3

Signal và Slot không khớp tham số.

Ví dụ:

Signal:

```text-x-trilium-auto
Signal(int)
```

Slot:

```text-x-trilium-auto
def update():
```

Sai.

Đúng:

```text-x-trilium-auto
def update(value):
```

---

## Lỗi 4

Để cửa sổ con sửa trực tiếp giao diện cửa sổ cha.

Điều này làm mã nguồn phụ thuộc chặt chẽ và khó bảo trì.

Nên:

```text-x-trilium-auto
Dialog

↓

Signal

↓

MainWindow
```

Thay vì:

```text-x-trilium-auto
Dialog

↓

MainWindow.label.setText(...)
```

---

# Bài tập thực hành

## Bài 1

Tạo 5 nút:

- Python
- Java
- Go
- Rust
- Kotlin

Tất cả dùng chung một hàm `show_language(name)`.

Yêu cầu:

- Dùng `partial` hoặc `lambda`.

---

## Bài 2

Tạo `QLineEdit`.

Nhấn nút:

Hiển thị nội dung bằng `lambda`.

---

## Bài 3

Tạo lớp:

```text-x-trilium-auto
class Counter(QObject)
```

Có Signal:

```text-x-trilium-auto
valueChanged = Signal(int)
```

Mỗi lần tăng giá trị:

Emit Signal.

---

## Bài 4

Tạo Dialog nhập tên.

MainWindow nhận tên bằng Signal.

Không được gọi trực tiếp:

```text-x-trilium-auto
parent.label.setText(...)
```

---

# Mini Project cuối buổi: Máy phát thông báo

Xây dựng ứng dụng gồm:

- Một `QLineEdit` nhập nội dung thông báo.
- Một nút **Phát thông báo**.
- Một `QLabel` hiển thị thông báo.

Yêu cầu:

- Tạo lớp `Notifier(QObject)`.
- Định nghĩa `messageChanged = Signal(str)`.
- Khi nhấn nút:
  - Đọc nội dung từ `QLineEdit`.
  - `emit()` Signal.
- `QLabel` cập nhật thông qua Slot kết nối với Signal, không cập nhật trực tiếp trong hàm xử lý nút.

---

# Tổng kết Buổi 7

Bạn đã học những kỹ thuật mà hầu hết các lập trình viên PySide6 chuyên nghiệp sử dụng:

- Sử dụng `lambda` để truyền tham số.
- Sử dụng `functools.partial` để tái sử dụng hàm.
- Tự tạo `Signal`.
- Phát Signal bằng `emit()`.
- Tạo `Slot` với `@Slot`.
- Thiết kế giao tiếp giữa nhiều cửa sổ thông qua Signal thay vì phụ thuộc trực tiếp.

Đây là nền tảng rất quan trọng để xây dựng các ứng dụng có kiến trúc rõ ràng, dễ mở rộng và dễ kiểm thử.

## Chuẩn bị cho Buổi 8

Ở **Buổi 8**, chúng ta sẽ chuyển sang chủ đề **Event System** của Qt, bao gồm:

- `mousePressEvent()`
- `mouseReleaseEvent()`
- `mouseMoveEvent()`
- `keyPressEvent()`
- `keyReleaseEvent()`
- `resizeEvent()`
- `closeEvent()`
- `paintEvent()`

Đây là bước giúp bạn hiểu cách Qt xử lý chuột, bàn phím, thay đổi kích thước cửa sổ và vẽ giao diện tùy chỉnh, mở đường cho việc xây dựng các ứng dụng tương tác và đồ họa chuyên sâu.
