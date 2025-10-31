#Tìm kiếm nâng cao
import sys, os, csv, pytest, logging
from selenium import webdriver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from TimKiem.pages.advanced_search_page import AdvancedSearchPage

logger = logging.getLogger(__name__)

def read_csv_data(file_path):
    with open(file_path, encoding="utf-8-sig") as f:  # <- dùng utf-8-sig để bỏ BOM
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            # loại bỏ khoảng trắng và ký tự xuống dòng trong key
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            data.append(clean_row)
        return data

@pytest.mark.parametrize("data", read_csv_data("TimKiem/data/filter_data.csv"))
def test_advanced_search(data):
    """Kiểm thử DDT cho Tìm kiếm nâng cao"""
    driver = webdriver.Chrome()
    search = AdvancedSearchPage(driver)

    try:
        search.open_page()
        search.select_sort(data["sort"])
        search.select_category(data["category"])
        search.select_tag(data["tag"])
        search.click_search()
        search.verify_results_loaded()
        logger.info(f" Bộ lọc '{data}' hoạt động đúng!")
    finally:
        search.close_browser()
