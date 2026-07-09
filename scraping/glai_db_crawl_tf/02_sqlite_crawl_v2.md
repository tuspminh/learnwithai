? cào truyện và quản lý truyện. mỗi nguồn cào có catalog, catalog có nhiều trang, các trang này mỗi khi cập nhật sẽ tăng và số truyện mới thêm vào ở trang đầu, mỗi trang sẽ có nhiều link truyện, mỗi truyện có title, author, img cover, link truyện, description, và list chapter, mỗi chapter có thể có hoặc không title, và có nội dung chương

---

Để đáp ứng yêu cầu quản lý **đa nguồn cào (Multi-source)** và cơ chế **cập nhật trang đầu** (trang mới nhất tăng dần, truyện mới luôn đẩy lên đầu), cấu trúc cơ sở dữ liệu SQLite3 cần được tối ưu hóa lại.

Dưới đây là thiết kế chi tiết hệ thống bảng dữ liệu và quy trình xử lý trạng thái (state) tối ưu bằng SQLite3.

---

**Sơ đồ thiết kế Cơ sở dữ liệu (SQLite3 Schema)**

Để liên kết dữ liệu theo đúng logic: `Nguồn (Source) -> Mục (Catalog) -> Trang (Page) -> Truyện (Story) -> Chương (Chapter)`, bạn tạo 5 bảng sau:

**1. Bảng sources (Quản lý các trang web truyện khác nhau)**

sql

```text-x-trilium-auto
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,          -- Ví dụ: 'TruyenFull', 'TangThuVien'
    base_url TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);
```

Hãy thận trọng khi sử dụng mã.

**2. Bảng catalogs (Mục truyện của từng nguồn)**

Một nguồn có thể có nhiều mục (Truyện chữ, Truyện tranh, Tiên hiệp, Ngôn tình...).

sql

```text-x-trilium-auto
CREATE TABLE catalogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    name TEXT NOT NULL,                  -- Ví dụ: 'Truyện Mới Cập Nhật', 'Tiên Hiệp'
    catalog_url TEXT NOT NULL,           -- URL gốc của mục đó
    FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE
);
```

Hãy thận trọng khi sử dụng mã.

**3. Bảng pages (Quản lý từng trang trong danh sách)**

Vì truyện mới luôn thêm vào **trang đầu**, công cụ của bạn sẽ quét liên tục trang đầu tiên (`page_number = 1`). Bảng này giúp lưu trữ lịch sử và trạng thái quét của từng trang.

sql

```text-x-trilium-auto
CREATE TABLE pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    catalog_id INTEGER NOT NULL,
    page_number INTEGER NOT NULL,
    url TEXT NOT NULL,
    state TEXT CHECK(state IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')) DEFAULT 'PENDING',
    error_message TEXT,
    updated_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (catalog_id) REFERENCES catalogs(id) ON DELETE CASCADE,
    UNIQUE(catalog_id, page_number) -- Đảm bảo không trùng lặp số trang trong một mục
);
```

Hãy thận trọng khi sử dụng mã.

**4. Bảng stories (Quản lý thông tin truyện)**

Lưu trữ thông tin chi tiết của truyện. Dùng `story_url` làm khóa duy nhất để tránh cào trùng khi truyện bị đẩy qua các trang khác nhau.

sql

```text-x-trilium-auto
CREATE TABLE stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    catalog_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    cover_url TEXT,
    story_url TEXT NOT NULL UNIQUE,       -- URL duy nhất để nhận diện truyện, tránh cào trùng
    description TEXT,
    state TEXT CHECK(state IN ('DISCOVERED', 'CRAWLING_CHAPTER_LIST', 'CRAWLING_CONTENT', 'COMPLETED', 'FAILED')) DEFAULT 'DISCOVERED',
    error_message TEXT,
    updated_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (catalog_id) REFERENCES catalogs(id) ON DELETE CASCADE
);
```

Hãy thận trọng khi sử dụng mã.

**5. Bảng chapters (Quản lý chương và nội dung)**

Cột `title` được phép nhận giá trị `NULL` vì một số truyện chỉ để "Chương 1", "Chương 2" mà không có tiêu đề phụ.

sql

```text-x-trilium-auto
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    story_id INTEGER NOT NULL,
    chapter_number REAL NOT NULL,         -- Số chương (để REAL hỗ trợ chương dạng 10.5, 100.1)
    title TEXT,                           -- Cho phép NULL nếu chương không có tiêu đề
    chapter_url TEXT NOT NULL UNIQUE,     -- Tránh trùng lặp chương
    content TEXT,                         -- Nội dung chữ của chương (TEXT trong SQLite không giới hạn độ dài)
    state TEXT CHECK(state IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')) DEFAULT 'PENDING',
    error_message TEXT,
    updated_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

-- Tạo chỉ mục (Index) tăng tốc khi truy vấn danh sách chương của một truyện
CREATE INDEX idx_chapters_story_id ON chapters(story_id);
```

Hãy thận trọng khi sử dụng mã.

---

**Thuật toán xử lý trạng thái (State Workflow) tối ưu cho việc "Cập nhật liên tục"**

Do truyện mới liên tục đẩy vào trang 1 và đẩy truyện cũ sang trang sau, bạn áp dụng quy trình xử lý state như sau để tool chạy mượt mà:

**Bước 1: Quét danh sách truyện (Scan Page 1)**

- Bạn cho tool cào liên tục `url` của trang đầu tiên (`page_number = 1`).
- Đọc tất cả link truyện có trên trang này.
- Thực hiện lệnh chèn dữ liệu dạng **INSERT OR IGNORE INTO stories...**.
  - Nếu link truyện **chưa tồn tại**: SQLite sẽ thêm mới truyện với trạng thái `DISCOVERED`.
  - Nếu link truyện **đã tồn tại**: SQLite sẽ tự động bỏ qua (không ghi đè, không làm mất trạng thái cũ của truyện đó).
- Nếu phát hiện trên trang 1 toàn bộ là truyện mới (chưa có trong DB), tăng số trang lên để quét tiếp trang 2, trang 3 cho đến khi gặp lại truyện cũ thì dừng lại.

**Bước 2: Cào danh sách chương (Get Chapter List)**

- Lọc các truyện có trạng thái `DISCOVERED` hoặc `CRAWLING_CHAPTER_LIST`.
- Chuyển trạng thái sang `CRAWLING_CHAPTER_LIST`.
- Vào link truyện để lấy danh sách toàn bộ link chương. Sử dụng **INSERT OR IGNORE INTO chapters...** để lưu link chương vào DB dưới trạng thái `PENDING`.
- Sau khi lấy xong danh sách chương, đổi trạng thái truyện sang `CRAWLING_CONTENT`.

**Bước 3: Cào nội dung chi tiết chương (Get Content)**

- Lọc các chương đang ở trạng thái `PENDING` hoặc `FAILED`.
- Đổi sang `PROCESSING`, tiến hành tải nội dung chữ (`content`).
- Lưu nội dung chữ vào DB và chuyển trạng thái chương sang `COMPLETED`. Nếu lỗi (mạng sập, chặn IP), chuyển sang `FAILED` kèm lý do lỗi để chạy lại sau.

**Bước 4: Kiểm tra hoàn thành (Chốt hạ)**

- Quét các truyện có trạng thái `CRAWLING_CONTENT`.
- Chạy câu lệnh kiểm tra xem còn chương nào thuộc truyện này có trạng thái `PENDING` hoặc `FAILED` không.
- Nếu **không còn**, cập nhật trạng thái truyện thành `COMPLETED`.

---

Nếu bạn muốn bắt tay vào code, bạn định sử dụng ngôn ngữ nào (**Python**, **Node.js**, hay **C#**)? Tôi có thể cung cấp đoạn mã mẫu (ví dụ: dùng Python `sqlite3` + `Playwright` / `BeautifulSoup`) xử lý chính xác logic `INSERT OR IGNORE` và cập nhật các State này cho bạn.
