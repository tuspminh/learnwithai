Để quản lý file ảnh khi xóa truyện, giải pháp tốt nhất là thực hiện thông qua code Python trước khi ra lệnh xóa hàng trong SQLite. Do SQLite không thể tự can thiệp vào hệ thống file của hệ điều hành để xóa file ảnh vật lý, chúng ta cần làm theo quy trình:

**Tìm đường dẫn ảnh -> Xóa file ảnh trên ổ cứng -> Xóa dữ liệu trong DB**.

Dưới đây là hàm Python tối ưu để xóa truyện (hoặc xóa toàn bộ mục truyện) mà không để lại "file rác" trong thư mục `covers`:

**1. Hàm xóa một truyện cụ thể (delete_story)**

Hàm này nhận vào `story_id`, tìm và xóa file ảnh bìa trước, sau đó xóa truyện trong DB. Nhờ cấu hình khóa ngoại `ON DELETE CASCADE` đã cài đặt ở các bước trước, **toàn bộ chương liên quan đến truyện này sẽ tự động bị xóa theo**.

python

```text-x-trilium-auto
import os
import sqlite3

DB_NAME = "story_crawler.db"

def delete_story(story_id):
    """Xóa một truyện theo ID, tự động xóa file ảnh bìa cục bộ và các chương liên quan."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;") # Bắt buộc phải bật để tự động xóa chương (CASCADE)
    cursor = conn.cursor()

    try:
        # 1. Lấy đường dẫn file ảnh bìa trước khi xóa dữ liệu
        cursor.execute("SELECT cover_path FROM stories WHERE id = ?", (story_id,))
        row = cursor.fetchone()

        # 2. Xóa file ảnh vật lý trên ổ cứng nếu file tồn tại
        if row and row[0]:
            cover_path = row[0]
            if os.path.exists(cover_path):
                os.remove(cover_path)
                print(f" Đã xóa file ảnh: {cover_path}")
            else:
                print(f" File ảnh {cover_path} không tồn tại trên ổ cứng (bỏ qua).")

        # 3. Xóa truyện trong Database
        cursor.execute("DELETE FROM stories WHERE id = ?", (story_id,))

        # Nếu xóa thành công
        if cursor.rowcount > 0:
            conn.commit()
            print(f" Thành công: Đã xóa truyện ID {story_id} và toàn bộ chương của truyện này khỏi DB.")
        else:
            print(f" Không tìm thấy truyện với ID {story_id} trong cơ sở dữ liệu.")

    except Exception as e:
        conn.rollback()
        print(f" Lỗi xảy ra khi xóa truyện: {e}")
    finally:
        conn.close()
```

Hãy thận trọng khi sử dụng mã.

---

**2. Hàm dọn dẹp hàng loạt (delete_catalog_or_source)**

Trong trường hợp bạn muốn xóa cả một **Mục truyện (Catalog)** hoặc một **Nguồn cào (Source)**, số lượng truyện bị xóa sẽ rất lớn. Chúng ta cần gom tất cả đường dẫn ảnh của các truyện bị ảnh hưởng để xóa một lượt trước khi hạ lệnh xóa trên DB.

python

```text-x-trilium-auto
def delete_catalog(catalog_id):
    """Xóa toàn bộ một mục truyện, dọn sạch tất cả file ảnh của các truyện thuộc mục đó."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    try:
        # 1. Tìm tất cả đường dẫn ảnh của các truyện thuộc danh mục này
        cursor.execute("SELECT cover_path FROM stories WHERE catalog_id = ?", (catalog_id,))
        rows = cursor.fetchall()

        # 2. Xóa hàng loạt file ảnh trên ổ cứng
        deleted_files_count = 0
        for row in rows:
            if row[0] and os.path.exists(row[0]):
                os.remove(row[0])
                deleted_files_count += 1

        print(f" Đã dọn dẹp {deleted_files_count} file ảnh của danh mục này.")

        # 3. Xóa danh mục trong DB (Sẽ tự động xóa toàn bộ câu chuyện và chương nhờ CASCADE)
        cursor.execute("DELETE FROM catalogs WHERE id = ?", (catalog_id,))
        conn.commit()
        print(f" Thành công: Đã xóa danh mục ID {catalog_id} và mọi dữ liệu liên quan.")

    except Exception as e:
        conn.rollback()
        print(f" Lỗi khi xóa danh mục: {e}")
    finally:
        conn.close()
```

Hãy thận trọng khi sử dụng mã.

---

**💡 Mẹo nâng cao: Hàm quét dọn file rác mồ côi (Orphaned Files)**

Trong quá trình vận hành tool cào, đôi khi tool bị tắt đột ngột hoặc xảy ra lỗi logic khiến file ảnh đã tải xuống thư mục `covers/` nhưng đường dẫn chưa kịp lưu vào DB (hoặc ngược lại).

Bạn có thể chạy hàm kiểm tra định kỳ này để tìm xem có file ảnh nào nằm trong thư mục `covers/` mà không có truyện nào trong DB sở hữu nó hay không, nếu có thì xóa đi để giải phóng bộ nhớ ổ cứng:

python

```text-x-trilium-auto
def clean_orphaned_covers():
    """Tìm và xóa các file ảnh trong thư mục 'covers' không liên kết với truyện nào trong DB."""
    if not os.path.exists("covers"):
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Lấy tất cả đường dẫn ảnh đang có trong DB
    cursor.execute("SELECT cover_path FROM stories WHERE cover_path IS NOT NULL")
    db_paths = set(row[0] for row in cursor.fetchall())
    conn.close()

    # Quét thư mục cục bộ
    local_files = os.listdir("covers")
    cleaned_count = 0

    for file in local_files:
        full_path = os.path.join("covers", file)

        # Nếu file trên ổ cứng không nằm trong danh sách đường dẫn của DB -> File rác
        if full_path not in db_paths:
            os.remove(full_path)
            cleaned_count += 1

    if cleaned_count > 0:
        print(f"🧹 Đã dọn dẹp {cleaned_count} file ảnh rác (mồ côi) trong thư mục covers.")
    else:
        print(" Thư mục ảnh sạch sẽ, không có file rác.")
```

Hãy thận trọng khi sử dụng mã.

Hệ thống quản lý của bạn hiện tại đã rất hoàn chỉnh và an toàn cho bộ nhớ ổ cứng. Tiếp theo, bạn có cần tích hợp thêm tính năng nào khác không, ví dụ như **xuất toàn bộ dữ liệu truyện (text + ảnh cục bộ) ra file EPUB/PDF để đọc offline**?
