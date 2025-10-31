import sys, os, pytest, csv, logging
from selenium import webdriver

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from TimKiem.pages.search_page import SearchPage

logger = logging.getLogger(__name__)

def read_csv_data(file_path):
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row["keyword"] for row in reader]

@pytest.mark.parametrize("keyword", read_csv_data("TimKiem/data/search_data.csv"))
def test_search_suggestions(keyword):
    """Kiểm thử gợi ý tìm kiếm (Data Driven Test)"""
    driver = webdriver.Chrome()
    search = SearchPage(driver)

    try:
        search.open_homepage()
        search.search_keyword(keyword)
        results = search.get_suggestions()

        assert any(keyword.lower() in r.lower() for r in results), f" Không tìm thấy gợi ý cho '{keyword}'!"
        logger.info(f" Có gợi ý hợp lệ cho '{keyword}'!")

    finally:
        search.close_browser()
