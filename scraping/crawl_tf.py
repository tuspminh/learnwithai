import requests
from bs4 import BeautifulSoup

def crawl_novel_links(): 
    # (base_url,catalog_slug):
    # page_url = "https://truyenfull.today/"
    # page_url = "https://truyenfull.today/danh-sach/truyen-full/"
    # page_url = "https://truyenfull.today/the-loai/ngon-tinh/"
    page_url = "https://truyenfull.today/danh-sach/truyen-moi/"
    # boc trong try, loi cao trang
    response = requests.get(page_url,headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    if response.status_code != 200:
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    # list truyện hot @ trang chu
    story_items = soup.select('div.container div.item[itemtype="https://schema.org/Book"]')
    print(f'{len(story_items) if story_items else 0} novels found')

    # default list truyện dùng selector này.
    story_items2 = soup.select('div.container div.row[itemtype="https://schema.org/Book"]')
    print(f'{len(story_items2) if story_items2 else 0} novels found')

    # list truyện @ trang chu
    story_items3 = soup.select('div.container div.row div.col-xs-4.col-sm-3.col-md-2')
    print(f'{len(story_items3) if story_items3 else 0} novels found')

    # phân trang, lấy max số đuôi của url ra số trang, lấy tiếp duyệt từ 2
    page_items = soup.select('div.container div.text-center.pagination-container ul.pagination.pagination-sm li a')
    print(f'{len(page_items) if page_items else 0} pages found')
    print(f'page_items: {"\n".join([item.get("href") for item in page_items])}')
    # duyệt phân trang trước, xong lấy duyệt từng page lấy hêt link

def crawl_novel(novel_url):
    pass


crawl_novel_links()
