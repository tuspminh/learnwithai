Lưu ảnh vào thư mục cục bộ và chỉ lưu đường dẫn (Path) vào database là phương pháp chuẩn công nghiệp. Cách này giữ cho file SQLite (`.db`) luôn nhỏ gọn, chạy nhanh và dễ dàng backup dữ liệu.

Dưới đây là cách chỉnh sửa database và mã nguồn Python để tự động tạo thư mục, tải ảnh, đặt tên theo ID truyện và lưu đường dẫn.

**1. Cấu trúc bảng stories mới (Lưu đường dẫn)**

Cột `cover_path` sẽ có kiểu dữ liệu là **TEXT** để lưu đường dẫn file cục bộ (ví dụ: `covers/story_1.jpg`).

sql

```text-x-trilium-auto
CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    catalog_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    cover_path TEXT,                    -- Lưu đường dẫn file cục bộ (Ví dụ: 'covers/1.jpg')
    story_url TEXT NOT NULL UNIQUE,
    description TEXT,
    state TEXT CHECK(state IN ('DISCOVERED', 'CRAWLING_CHAPTER_LIST', 'CRAWLING_CONTENT', 'COMPLETED', 'FAILED')) DEFAULT 'DISCOVERED',
    error_message TEXT,
    updated_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (catalog_id) REFERENCES catalogs(id) ON DELETE CASCADE
);
```

Hãy thận trọng khi sử dụng mã.

---

**2. Cập nhật Code Python (Tải và quản lý file ảnh cục bộ)**

Vì chúng ta cần dùng **id của truyện** để đặt tên cho file ảnh (tránh trùng tên file và dễ quản lý), quy trình lưu ảnh sẽ được thực hiện ngay **sau khi** chèn truyện vào DB.

python

```text-x-trilium-auto
import os
import sqlite3
import requests
from bs4 import BeautifulSoup

# Tạo thư mục lưu trữ ảnh nếu chưa tồn tại
IMAGE_DIR = "covers"
os.makedirs(IMAGE_DIR, exist_ok=True)

def crawl_catalog_page(catalog_id, page_number):
    conn = sqlite3.connect("story_crawler.db")
    cursor = conn.cursor()

    # (Đoạn code gọi requests và khởi tạo BeautifulSoup giữ nguyên)
    story_items = soup.select(".story-item") 
    new_stories_count = 0

    for item in story_items:
        title = item.select_one(".title").text.strip()
        story_url = item.select_one("a")["href"]
        author = item.select_one(".author").text.strip() if item.select_one(".author") else "Ẩn danh"
        desc = item.select_one(".desc").text.strip() if item.select_one(".desc") else ""
        cover_url = item.select_one("img")["src"] if item.select_one("img") else None

        # Bước 1: Chèn truyện vào DB trước (Chưa có ảnh bìa)
        # Sử dụng INSERT OR IGNORE để tránh trùng lặp link truyện
        cursor.execute("""
            INSERT OR IGNORE INTO stories (catalog_id, title, author, story_url, description, state)
            VALUES (?, ?, ?, ?, ?, 'DISCOVERED')
        """, (catalog_id, title, author, story_url, desc))

        # Bước 2: Nếu đây là truyện mới (chèn thành công), tiến hành lấy ID để tải ảnh
        if cursor.rowcount > 0:
            new_stories_count += 1
            story_id = cursor.lastrowid # Lấy ID tự động tăng vừa sinh ra

            if cover_url:
                try:
                    # Tải dữ liệu ảnh từ internet
                    img_response = requests.get(cover_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                    if img_response.status_code == 200:

                        # Lấy phần mở rộng của ảnh (ví dụ: .jpg, .png). Nếu không lấy được, mặc định là .jpg
                        ext = os.path.splitext(cover_url.split('?')[0])[1]
                        if ext.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
                            ext = '.jpg'

                        # Đặt tên file theo ID: covers/story_1.jpg
                        filename = f"story_{story_id}{ext}"
                        local_path = os.path.join(IMAGE_DIR, filename)

                        # Ghi file ảnh xuống ổ cứng (chế độ 'wb' - Write Binary)
                        with open(local_path, "wb") as f:
                            f.write(img_response.content)

                        # Cập nhật ngược lại đường dẫn file ảnh vào DB cho truyện này
                        cursor.execute("""
                            UPDATE stories SET cover_path = ? WHERE id = ?
                        """, (local_path, story_id))

                except Exception as e:
                    print(f" Lỗi khi tải ảnh bìa cho truyện ID {story_id}: {e}")
                    # Nếu lỗi, cột cover_path vẫn giữ giá trị NULL trong DB

    conn.commit()
    conn.close()
    return new_stories_count > 0
```

Hãy thận trọng khi sử dụng mã.

---

**💡 Lợi ích và cách hiển thị sau này:**

1. **Cấu trúc thư mục ngăn nắp:** Trong thư mục dự án của bạn sẽ xuất hiện một thư mục tên là `covers/`. Bên trong chứa các file: `story_1.jpg`, `story_2.png`, `story_3.jpg`... cực kỳ dễ quản lý.
2. **Khi hiển thị lên Giao diện (Web/App):** Bạn chỉ cần đọc cột `cover_path` từ DB.
  - Nếu dùng thư viện Web (như Flask/FastAPI), bạn chỉ cần cấu hình thư mục `covers` thành thư mục chứa file tĩnh (Static folder).
  - Nếu hiển thị trên ứng dụng máy tính (Desktop App), bạn chỉ cần truyền trực tiếp đường dẫn `covers/story_1.jpg` vào component hiển thị ảnh là xong.

Bạn có cần tối ưu thêm phần **xử lý khi xóa truyện** không? (Ví dụ: Viết một hàm khi xóa 1 hàng trong DB thì code Python tự động xóa luôn file ảnh vật lý tương ứng trong thư mục `covers` để tránh rác ổ cứng).
