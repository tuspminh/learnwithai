? cào danh sách truyện, cào truyện và quản lý truyện, có state của từng chương, truyện và page list

Để xây dựng một hệ thống cào và quản lý truyện sử dụng SQLite3, bạn cần thiết kế các bảng dữ liệu quản lý chặt chẽ trạng thái (**state**) từ cấp độ Danh sách trang (Page list) -> Truyện (Story) -> Chương (Chapter).

Dưới đây là sơ đồ thiết kế cơ sở dữ liệu (Database Schema) tối ưu bằng SQLite3 giúp bạn dễ dàng theo dõi tiến độ cào, tránh cào trùng và có thể tiếp tục cào lại khi lỗi (Resume/Retry).

**1. Bảng page_lists (Quản lý phân trang danh sách truyện)**

Bảng này lưu danh sách các trang chứa danh sách truyện (ví dụ: `://truyen.com`, `page=2`).

sql

```text-x-trilium-auto
CREATE TABLE page_lists (
    page_number INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    state TEXT CHECK(state IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')) DEFAULT 'PENDING',
    error_message TEXT,
    updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);
```

- **State**:
  - `PENDING`: Chưa cào.
  - `PROCESSING`: Đang đọc danh sách truyện trên trang này.
  - `COMPLETED`: Đã lấy hết toàn bộ link truyện của trang này.

**2. Bảng stories (Quản lý thông tin truyện)**

Lưu thông tin tổng quan của truyện được phát hiện từ các trang danh sách.

sql

```text-x-trilium-auto
CREATE TABLE stories (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title TEXT NOT NULL,
    story_url TEXT NOT NULL UNIQUE,
    author TEXT,
    cover_url TEXT,
    description TEXT,
    state TEXT CHECK(state IN ('DISCOVERED', 'CRAWLING', 'COMPLETED', 'FAILED')) DEFAULT 'DISCOVERED',
    error_message TEXT,
    updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);
```

Hãy thận trọng khi sử dụng mã.

- **State**:
  - `DISCOVERED`: Mới tìm thấy link, chưa cào chi tiết.
  - `CRAWLING`: Đang cào danh sách chương hoặc đang cào nội dung chương.
  - `COMPLETED`: Đã cào thành công toàn bộ các chương hiện tại.

**3. Bảng chapters (Quản lý nội dung và trạng thái từng chương)**

Bảng này liên kết với bảng truyện, lưu nội dung chữ và trạng thái cào của từng chương đơn lẻ.

sql

```text-x-trilium-auto
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    story_id INTEGER NOT NULL,
    chapter_number REAL NOT NULL, -- Dùng REAL để xử lý chương dạng 10.5
    title TEXT NOT NULL,
    chapter_url TEXT NOT NULL UNIQUE,
    content TEXT, -- Nội dung chữ của truyện (Kiểu TEXT không giới hạn độ dài)
    state TEXT CHECK(state IN ('PENDING', 'COMPLETED', 'FAILED')) DEFAULT 'PENDING',
    error_message TEXT,
    updated_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);
-- Tạo Index để tối ưu tốc độ tìm kiếm chương theo truyện
CREATE INDEX idx_chapters_story ON chapters(story_id);
```

- **State**:
  - `PENDING`: Chương đã được tìm thấy nhưng chưa cào nội dung (`content` đang NULL).
  - `COMPLETED`: Đã cào nội dung thành công.
  - `FAILED`: Lỗi tải trang, lỗi proxy, chặn IP... cần cào lại chương này.

---

**Quy trình cập nhật trạng thái (State Workflow) khi code Tool Cào**

1. **Bước 1 (Cào Page List):** Lấy danh sách `page_lists` có state = `PENDING`. Đổi sang `PROCESSING`. Cào xong, trích xuất tất cả link truyện chèn vào bảng `stories` dưới dạng `DISCOVERED`, sau đó đổi state của page đó thành `COMPLETED`.
2. **Bước 2 (Cào Danh sách chương):** Quét các truyện có state = `DISCOVERED`. Đổi sang `CRAWLING`. Vào link truyện để lấy toàn bộ danh sách link chương, chèn vào bảng `chapters` dạng `PENDING`.
3. **Bước 3 (Cào Nội dung chương):** Tìm các chương có state = `PENDING` (hoặc `FAILED` nếu muốn cào lại). Tải nội dung text, lưu vào cột `content`, đổi state chương sang `COMPLETED`.
4. **Bước 4 (Chốt hạ):** Khi tất cả các chương của một `story_id` đều là `COMPLETED`, cập nhật state của truyện đó trong bảng `stories` thành `COMPLETED`.

Nếu bạn muốn tiếp tục triển khai, hãy cho tôi biết:

- Bạn định viết tool cào bằng ngôn ngữ nào (**Python/Node.js/C#**)?
- Bạn có cần tôi viết mẫu đoạn code **Python (BeautifulSoup/Playwright + Sqlite3)** để demo quy trình chuyển đổi trạng thái này không?
