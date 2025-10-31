import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("artifacts/search_test.log", mode="w", encoding="utf-8")
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://hangtruyen.top/"
        self.search_input = (By.CSS_SELECTOR, "input[placeholder='Tìm kiếm']")
        self.suggest_list = (By.CSS_SELECTOR, "ul.result li")

    def open_homepage(self):
        logger.info(" Mở trang chủ HangTruyen...")
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        time.sleep(2)

    def search_keyword(self, keyword):
        logger.info(f" Gõ từ khóa tìm kiếm: {keyword}")
        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.search_input)
        )
        search_box.clear()
        search_box.send_keys(keyword)
        time.sleep(2)  # chờ gợi ý hiển thị

    def get_suggestions(self):
        """Trả về danh sách các tiêu đề gợi ý"""
        try:
            suggestions = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(self.suggest_list)
            )
            results = [s.text for s in suggestions if s.text.strip()]
            logger.info(f" Có {len(results)} gợi ý: {results[:5]}...")
            return results
        except Exception:
            logger.warning(" Không có gợi ý nào hiển thị.")
            return []

    def close_browser(self):
        self.driver.quit()
        logger.info(" Đã đóng trình duyệt.")
