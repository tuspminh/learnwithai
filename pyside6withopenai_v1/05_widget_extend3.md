# PySide6 - Buổi 5

# QTableWidget, QTabWidget, QFileDialog, QDateEdit và ứng dụng Quản lý sinh viên

Đây là buổi học rất quan trọng vì bạn sẽ bắt đầu làm việc với **dữ liệu dạng bảng**, nền tảng của hầu hết các ứng dụng quản lý.

---

# Mục tiêu

Sau buổi học này, bạn sẽ biết cách sử dụng:

- `QTableWidget`
- `QTableWidgetItem`
- `QHeaderView`
- `QTabWidget`
- `QFrame`
- `QSplitter`
- `QDateEdit`
- `QFileDialog`
- Xây dựng ứng dụng Quản lý sinh viên

---

# 1. QTableWidget

`QTableWidget` dùng để hiển thị dữ liệu theo dạng bảng.

Ví dụ:

| Mã SV | Họ tên | Lớp |
| --- | --- | --- |
| SV001 | Nguyễn Văn A | CNTT1 |
| SV002 | Trần Văn B | CNTT2 |

---

## Tạo bảng

```text-x-trilium-auto
table = QTableWidget()
```

---

## Thiết lập số hàng và cột

```text-x-trilium-auto
table.setRowCount(5)
table.setColumnCount(3)
```

---

## Đặt tiêu đề cột

```text-x-trilium-auto
table.setHorizontalHeaderLabels([
    "Mã",
    "Tên",
    "Lớp"
])
```

---

## Thêm dữ liệu

```text-x-trilium-auto
table.setItem(
    0,
    0,
    QTableWidgetItem("SV001")
)
```

---

Ví dụ đầy đủ

```text-x-trilium-auto
from PySide6.QtWidgets import *

app = QApplication([])

table = QTableWidget()

table.setColumnCount(3)

table.setRowCount(2)

table.setHorizontalHeaderLabels([
    "Mã",
    "Tên",
    "Lớp"
])

table.setItem(0,0,QTableWidgetItem("SV001"))
table.setItem(0,1,QTableWidgetItem("Nguyễn Văn A"))
table.setItem(0,2,QTableWidgetItem("CNTT1"))

table.setItem(1,0,QTableWidgetItem("SV002"))
table.setItem(1,1,QTableWidgetItem("Trần Văn B"))
table.setItem(1,2,QTableWidgetItem("CNTT2"))

table.show()

app.exec()
```

---

# 2. Tự động giãn cột

```text-x-trilium-auto
table.horizontalHeader().setSectionResizeMode(
    QHeaderView.Stretch
)
```

Kết quả:

```text-x-trilium-auto
+-----------------------------+
| Mã | Tên | Lớp |
+-----------------------------+
```

Các cột luôn đầy chiều ngang.

---

# 3. Thêm hàng động

```text-x-trilium-auto
row = table.rowCount()

table.insertRow(row)
```

Sau đó:

```text-x-trilium-auto
table.setItem(
    row,
    0,
    QTableWidgetItem("SV003")
)
```

---

# 4. Xóa hàng

```text-x-trilium-auto
row = table.currentRow()

table.removeRow(row)
```

---

# 5. Lấy dữ liệu ô

```text-x-trilium-auto
item = table.item(0,1)

print(item.text())
```

---

# 6. QTabWidget

Tạo giao diện nhiều tab.

Ví dụ:

```text-x-trilium-auto
------------------------

Thông tin | Danh sách

------------------------
```

---

Tạo:

```text-x-trilium-auto
tabs = QTabWidget()
```

---

Thêm tab

```text-x-trilium-auto
tabs.addTab(widget1,"Thông tin")
tabs.addTab(widget2,"Danh sách")
```

---

# 7. QFrame

Dùng để tạo khung.

```text-x-trilium-auto
frame = QFrame()

frame.setFrameShape(
    QFrame.Box
)
```

Có thể dùng để nhóm các thành phần mà không cần `QGroupBox`.

---

# 8. QSplitter

Cho phép người dùng kéo thay đổi kích thước giữa hai vùng.

Ví dụ:

```text-x-trilium-auto
Danh sách | Chi tiết
```

Tạo:

```text-x-trilium-auto
splitter = QSplitter()

splitter.addWidget(left)

splitter.addWidget(right)
```

---

# 9. QDateEdit

Dùng để nhập ngày tháng.

```text-x-trilium-auto
date = QDateEdit()
```

Hiển thị lịch:

```text-x-trilium-auto
date.setCalendarPopup(True)
```

Ngày hiện tại:

```text-x-trilium-auto
from PySide6.QtCore import QDate

date.setDate(QDate.currentDate())
```

Lấy giá trị:

```text-x-trilium-auto
print(date.date().toString("dd/MM/yyyy"))
```

---

# 10. QFileDialog

Chọn tệp hoặc thư mục.

## Mở tệp

```text-x-trilium-auto
filename, _ = QFileDialog.getOpenFileName(
    self,
    "Chọn file"
)
```

---

## Lưu tệp

```text-x-trilium-auto
filename, _ = QFileDialog.getSaveFileName(
    self,
    "Lưu file"
)
```

---

## Chọn thư mục

```text-x-trilium-auto
folder = QFileDialog.getExistingDirectory(
    self,
    "Chọn thư mục"
)
```

---

# Mini Project 1

## Chọn ảnh

```text-x-trilium-auto
file, _ = QFileDialog.getOpenFileName(
    self,
    "Chọn ảnh",
    "",
    "Image (*.png *.jpg)"
)
```

Sau đó hiển thị đường dẫn bằng `QLabel`.

---

# Dự án Buổi 5: Quản lý sinh viên

## Giao diện

```text-x-trilium-auto
-------------------------------------------------

Thông tin | Danh sách

-------------------------------------------------

Tab Thông tin

Mã SV

[________]

Tên

[________]

Ngày sinh

[01/01/2025]

Lớp

[________]

[Thêm]

-------------------------------------------------

Tab Danh sách

+---------------------------------------------+

| Mã | Tên | Ngày sinh | Lớp |

+---------------------------------------------+

[Xóa]

-------------------------------------------------
```

---

## Ý tưởng triển khai

- Tab **Thông tin**:
  - `QLineEdit` cho mã sinh viên, tên, lớp.
  - `QDateEdit` cho ngày sinh.
  - Nút **Thêm** để thêm sinh viên.
- Tab **Danh sách**:
  - `QTableWidget` hiển thị toàn bộ sinh viên.
  - Nút **Xóa** để xóa dòng đang chọn.

---

## Gợi ý cấu trúc lớp

```text-x-trilium-auto
class StudentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.create_ui()
        self.create_form_tab()
        self.create_table_tab()
        self.connect_signals()

    def create_ui(self):
        ...

    def create_form_tab(self):
        ...

    def create_table_tab(self):
        ...

    def connect_signals(self):
        ...

    def add_student(self):
        ...

    def delete_student(self):
        ...
```

Cách chia nhỏ phương thức như trên giúp mã nguồn rõ ràng, dễ bảo trì và mở rộng.

---

# Bài tập

### Bài 1

Hoàn thiện ứng dụng **Quản lý sinh viên**:

- Thêm sinh viên.
- Xóa sinh viên.
- Tự động đánh số thứ tự (STT).

---

### Bài 2

Khi nhấp vào một dòng trong bảng:

- Hiển thị thông tin lên các ô nhập ở tab **Thông tin**.
- Cho phép chỉnh sửa rồi cập nhật lại dữ liệu.

---

### Bài 3

Thêm nút **Lưu CSV**:

- Mở `QFileDialog` để chọn nơi lưu.
- Ghi toàn bộ dữ liệu từ `QTableWidget` ra tệp CSV bằng mô-đun `csv`.

---

# Kiến thức cần nhớ

| Widget/Lớp | Công dụng |
| --- | --- |
| `QTableWidget` | Hiển thị dữ liệu dạng bảng |
| `QTableWidgetItem` | Một ô trong bảng |
| `QHeaderView` | Điều khiển tiêu đề và kích thước cột |
| `QTabWidget` | Giao diện nhiều tab |
| `QFrame` | Tạo khung |
| `QSplitter` | Chia giao diện có thể kéo giãn |
| `QDateEdit` | Chọn ngày |
| `QFileDialog` | Chọn hoặc lưu tệp |

---

## Dự án xuyên suốt khóa học

Từ buổi 5 trở đi, chúng ta sẽ xây dựng một **ứng dụng quản lý hoàn chỉnh** theo từng bước:

- **Buổi 5:** Quản lý sinh viên với `QTableWidget`.
- **Buổi 6:** Chia dự án thành nhiều tệp, sử dụng `QMenuBar`, `QToolBar`, `QStatusBar` và kiến trúc rõ ràng.
- **Buổi 7:** Tích hợp **SQLite** để lưu dữ liệu thay vì chỉ lưu trong bộ nhớ.
- **Buổi 8:** Tìm kiếm, lọc, sắp xếp và xuất/nhập dữ liệu.
- **Buổi 9:** Sử dụng **Qt Designer** và tệp `.ui`.
- **Buổi 10:** Đóng gói ứng dụng thành file thực thi và áp dụng các kỹ thuật nâng cao.

Đến cuối giai đoạn này, bạn sẽ có nền tảng vững chắc để phát triển các ứng dụng desktop như quản lý bán hàng, quản lý thư viện, ứng dụng học từ vựng hoặc công cụ TTS bằng PySide6.
