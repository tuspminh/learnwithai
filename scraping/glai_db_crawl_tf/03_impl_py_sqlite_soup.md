Dưới đây là mã nguồn Python hoàn chỉnh sử dụng `sqlite3` và `BeautifulSoup` (kết hợp `requests`). Mã nguồn này hiện thực hóa toàn bộ logic quản lý trạng thái (State Workflow), cơ chế chống cào trùng (`INSERT OR IGNORE`) và xử lý việc cập nhật truyện mới ở trang đầu như đã phân tích. [[1](https://www.webscrapingapi.com/python-beautifulsoup-web-scraper), [2](https://felix-pappe.medium.com/breaking-isolation-a-practical-guide-to-building-an-mcp-server-with-sqlite-68c800a25d42), [3](https://stackoverflow.com/questions/39963972/python-how-to-simulate-a-click-using-beautifulsoup)]

**1. File khởi tạo Database (init_db.py)**

Chạy file này một lần duy nhất để tạo cấu trúc bảng và chèn dữ liệu cấu hình nguồn cào ban đầu. [[1](https://medium.com/@ccpythonprogramming/mimicking-googles-search-speed-with-sqlite-and-python-7b756ae82732)]

python

```text-x-trilium-auto
import sqlite3

def init_database():
    conn = sqlite3.connect("story_crawler.db")
    cursor = conn.cursor()

    # Bật tính năng khóa ngoại (Foreign Keys) trong SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Bảng nguồn
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        base_url TEXT NOT NULL
    );""")

    # 2. Bảng mục truyện
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS catalogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        catalog_url TEXT NOT NULL,
        FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE
    );""")

    # 3. Bảng truyện
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        catalog_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        author TEXT,
        cover_url TEXT,
        story_url TEXT NOT NULL UNIQUE,
        description TEXT,
        state TEXT CHECK(state IN ('DISCOVERED', 'CRAWLING_CHAPTER_LIST', 'CRAWLING_CONTENT', 'COMPLETED', 'FAILED')) DEFAULT 'DISCOVERED',
        error_message TEXT,
        updated_at TEXT DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (catalog_id) REFERENCES catalogs(id) ON DELETE CASCADE
    );""")

    # 4. Bảng chương
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_id INTEGER NOT NULL,
        chapter_number REAL NOT NULL,
        title TEXT,
        chapter_url TEXT NOT NULL UNIQUE,
        content TEXT,
        state TEXT CHECK(state IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')) DEFAULT 'PENDING',
        error_message TEXT,
        updated_at TEXT DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
    );""")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_chapters_story_id ON chapters(story_id);")

    # Ghi dữ liệu mẫu (Giả lập một trang web truyện)
    cursor.execute("INSERT OR IGNORE INTO sources (id, name, base_url) VALUES (1, 'WebTruyenX', 'https://example.com')")
    cursor.execute("INSERT OR IGNORE INTO catalogs (id, source_id, name, catalog_url) VALUES (1, 1, 'Truyện Mới Cập Nhật', 'https://example.com')")

    conn.commit()
    conn.close()
    print(" Khởi tạo cơ sở dữ liệu thành công!")

if __name__ == "__main__":
    init_database()
```

Hãy thận trọng khi sử dụng mã.

**2. File Script Cào và Quản lý State (crawler.py)**

Đoạn code này chứa các hàm cốt lõi để xử lý logic cào. Các hàm bóc tách HTML (`BeautifulSoup`) bên dưới đang để ở dạng giả lập (Selector ví dụ). Bạn chỉ cần thay thế đúng Selector CSS của trang web bạn cần cào.

python

```text-x-trilium-auto
import sqlite3
import requests
from bs4 import BeautifulSoup
import time

DB_NAME = "story_crawler.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ==========================================
# BƯỚC 1: CÀO TRANG DANH SÁCH (PAGE LIST)
# ==========================================
def crawl_catalog_page(catalog_id, page_number):
    """
    Cào một trang danh sách. Nếu phát hiện toàn bộ truyện trên trang này 
    đều đã có trong DB (truyện cũ bị đẩy xuống), hàm sẽ trả về False để dừng cào tiếp.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Lấy URL cấu hình của Catalog
    cursor.execute("SELECT catalog_url FROM catalogs WHERE id = ?", (catalog_id,))
    base_catalog_url = cursor.fetchone()[0]
    page_url = f"{base_catalog_url}{page_number}"

    print(f" Đang quét danh sách tại: {page_url}")

    try:
        response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code != 200:
            return False

        soup = BeautifulSoup(response.text, 'html.parser')

        # GIẢ LẬP: Tìm danh sách các item truyện trên trang
        story_items = soup.select(".story-item") 

        if not story_items:
            print(" Không tìm thấy truyện nào trên trang này. Dừng lại.")
            return False

        new_stories_count = 0

        for item in story_items:
            # Trích xuất thông tin bằng BeautifulSoup (Thay đổi selector theo thực tế)
            title = item.select_one(".title").text.strip()
            story_url = item.select_one("a")["href"]
            author = item.select_one(".author").text.strip() if item.select_one(".author") else "Ẩn danh"
            cover_url = item.select_one("img")["src"] if item.select_one("img") else ""
            desc = item.select_one(".desc").text.strip() if item.select_one(".desc") else ""

            # Sử dụng INSERT OR IGNORE: Nếu trùng story_url, SQLite sẽ tự bỏ qua
            cursor.execute("""
                INSERT OR IGNORE INTO stories (catalog_id, title, author, cover_url, story_url, description, state)
                VALUES (?, ?, ?, ?, ?, ?, 'DISCOVERED')
            """, (catalog_id, title, author, cover_url, story_url, desc))

            # Nếu vừa chèn thành công (thay đổi dòng), tăng biến đếm
            if cursor.rowcount > 0:
                new_stories_count += 1

        conn.commit()
        print(f"-> Đã thêm mới {new_stories_count}/{len(story_items)} truyện vào DB.")

        # Logic cập nhật: Nếu trang này không chứa bất kỳ truyện mới nào (new_stories_count == 0),
        # nghĩa là chúng ta đã đuổi kịp dữ liệu cũ -> Trả về False để không cần cào các trang tiếp theo (Page 2, 3...)
        return new_stories_count > 0

    except Exception as e:
        print(f" Lỗi khi cào trang danh sách: {e}")
        return False
    finally:
        conn.close()

# ==========================================
# BƯỚC 2: CÀO DANH SÁCH CHƯƠNG (CHAPTER LIST)
# ==========================================
def crawl_story_chapter_list():
    """ Tìm các truyện mới 'DISCOVERED' để lấy danh sách chương """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Lấy các truyện cần cào danh sách chương
    cursor.execute("SELECT id, story_url FROM stories WHERE state = 'DISCOVERED' LIMIT 5")
    stories_to_crawl = cursor.fetchall()

    for story_id, story_url in stories_to_crawl:
        print(f" Đang lấy danh sách chương của truyện ID {story_id}: {story_url}")

        # Cập nhật trạng thái sang CRAWLING_CHAPTER_LIST để tránh luồng khác cào trùng
        cursor.execute("UPDATE stories SET state = 'CRAWLING_CHAPTER_LIST' WHERE id = ?", (story_id,))
        conn.commit()

        try:
            response = requests.get(story_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # GIẢ LẬP: Tìm danh sách các link chương
            chapter_items = soup.select(".chapter-item a") 

            for index, ch_item in enumerate(chapter_items, start=1):
                ch_title = ch_item.text.strip() # Có thể có hoặc không có tiêu đề phụ
                ch_url = ch_item["href"]
                ch_number = index # Số chương tăng dần

                # INSERT OR IGNORE: Tránh trùng lặp chương
                cursor.execute("""
                    INSERT OR IGNORE INTO chapters (story_id, chapter_number, title, chapter_url, state)
                    VALUES (?, ?, ?, ?, 'PENDING')
                """, (story_id, ch_number, ch_title, ch_url))

            # Đổi trạng thái truyện sang giai đoạn: Chờ cào nội dung chữ
            cursor.execute("UPDATE stories SET state = 'CRAWLING_CONTENT', error_message = NULL WHERE id = ?", (story_id,))
            print(f"-> Thành công. Tìm thấy {len(chapter_items)} chương.")

        except Exception as e:
            cursor.execute("UPDATE stories SET state = 'FAILED', error_message = ? WHERE id = ?", (str(e), story_id))
            print(f" Thất bại khi lấy danh sách chương: {e}")

        conn.commit()
    conn.close()

# ==========================================
# BƯỚC 3: CÀO NỘI DUNG CHI TIẾT TỪNG CHƯƠNG
# ==========================================
def crawl_chapter_content():
    """ Lấy các chương đang 'PENDING' hoặc 'FAILED' để cào nội dung text """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Lấy ra 10 chương đang đợi cào
    cursor.execute("SELECT id, story_id, chapter_url FROM chapters WHERE state IN ('PENDING', 'FAILED') LIMIT 10")
    chapters_to_crawl = cursor.fetchall()

    for ch_id, story_id, ch_url in chapters_to_crawl:
        print(f" Đang cào nội dung chương ID {ch_id}: {ch_url}")

        cursor.execute("UPDATE chapters SET state = 'PROCESSING' WHERE id = ?", (ch_id,))
        conn.commit()

        try:
            response = requests.get(ch_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # GIẢ LẬP: Lấy cục văn bản nội dung truyện
            content_div = soup.select_one(".chapter-content")
            content_text = content_div.get_text(separator="\n").strip() if content_div else ""

            if not content_text:
                raise Exception("Không tìm thấy nội dung chữ (gặp mã Captcha hoặc lỗi Selector)")

            # Lưu nội dung chữ thành công
            cursor.execute("""
                UPDATE chapters 
                SET content = ?, state = 'COMPLETED', error_message = NULL, updated_at = datetime('now', 'localtime')
                WHERE id = ?
            """, (content_text, ch_id))

        except Exception as e:
            cursor.execute("""
                UPDATE chapters 
                SET state = 'FAILED', error_message = ?, updated_at = datetime('now', 'localtime')
                WHERE id = ?
            """, (str(e), ch_id))
            print(f"-> Lỗi chương {ch_id}: {e}")

        conn.commit()
        time.sleep(1) # Tránh bị chặn IP (Rate limit)

    conn.close()

# ==========================================
# BƯỚC 4: KIỂM TRA HOÀN THÀNH TRUYỆN (CHỐT HẠ)
# ==========================================
def check_and_complete_stories():
    """ Quét các truyện đang cào nội dung, nếu không còn chương nào trống/lỗi thì đóng trạng thái truyện """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tìm các truyện đang ở trạng thái cào nội dung
    cursor.execute("SELECT id FROM stories WHERE state = 'CRAWLING_CONTENT'")
    active_stories = cursor.fetchall()

    for (story_id,) in active_stories:
        # Kiểm tra xem truyện này có còn chương nào CHƯA hoàn thành không
        cursor.execute("""
            SELECT COUNT(*) FROM chapters 
            WHERE story_id = ? AND state IN ('PENDING', 'PROCESSING', 'FAILED')
        """, (story_id,))

        unfinished_count = cursor.fetchone()[0]

        # Nếu số chương chưa xong bằng 0 -> Truyện này đã cào hoàn tất hoàn toàn!
        if unfinished_count == 0:
            cursor.execute("UPDATE stories SET state = 'COMPLETED' WHERE id = ?", (story_id,))
            print(f" Chúc mừng: Truyện ID {story_id} đã hoàn thành toàn bộ các chương!")

    conn.commit()
    conn.close()

# ==========================================
# HÀM ĐIỀU KHIỂN CHÍNH (MAIN WORKFLOW)
# ==========================================
def run_crawler():
    print("\n--- BẮT ĐẦU VÒNG LẶP CÀO TRUYỆN ---")

    # 1. Cào trang danh sách (Kiểm tra liên tục trang 1 để lấy truyện mới cập nhật)
    catalog_id = 1
    page = 1
    while True:
        has_new_story = crawl_catalog_page(catalog_id, page)
        # Nếu trang hiện tại không có truyện mới nào (đều trùng lặp dữ liệu cũ) -> Ngừng lặp chuyển bước tiếp theo
        if not has_new_story:
            print(" Đã đuổi kịp dữ liệu cũ ở trang đầu. Dừng quét phân trang.")
            break
        page += 1
        time.sleep(2)

    # 2. Phân tích danh sách chương cho các truyện mới phát hiện
    crawl_story_chapter_list()

    # 3. Tiến hành tải nội dung chữ cho các chương
    crawl_chapter_content()

    # 4. Đồng bộ hóa và cập nhật trạng thái kết thúc cho truyện
    check_and_complete_stories()

    print("--- HOÀN THÀNH MỘT PHIÊN LÀM VIỆC ---\n")

if __name__ == "__main__":
    run_crawler()
```

Hãy thận trọng khi sử dụng mã.

**Cách thức vận hành tối ưu của Tool:**

1. **Chống cào trùng thông minh:** Hàm `crawl_catalog_page` liên tục bắn yêu cầu vào `page=1`. Khi một bộ truyện cũ bị đẩy lùi từ trang 1 sang trang 2, lệnh `INSERT OR IGNORE` sẽ kích hoạt giữ nguyên trạng thái cũ trong DB, đồng thời vòng lặp `while True` lập tức ngắt (`break`) giúp tool không cần duyệt vô nghĩa hàng ngàn trang phía sau.
2. **Xử lý sự cố (Resume Capability):** Nếu đang tải dở nội dung chương 50 mà mất mạng, trạng thái chương đó sẽ là `FAILED`. Khi bạn chạy lại tool vào lần sau, hàm `crawl_chapter_content` sẽ ưu tiên lọc lại các trạng thái `FAILED` này để tải bù dữ liệu. [[1](https://www.digitalocean.com/community/questions/how-to-set-up-persistent-sqlite3-file-and-logs-file-when-deploying-python-app-to-app-platform)]

Bạn có muốn bổ sung thêm cơ chế **quét lặp lại định kỳ (Scheduler)** sau mỗi 15 phút hoặc tích hợp hệ thống tự động đổi **Proxy/User-Agent** để né tránh việc bị trang truyện chặn IP (Ban IP) không?
