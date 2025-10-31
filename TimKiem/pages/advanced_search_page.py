import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("artifacts/advanced_search.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class AdvancedSearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://hangtruyen.top/tim-kiem"
        self.sort_dropdown = (By.CSS_SELECTOR, "#dd-sort .dropdown-toggle")
        self.sort_option = (By.CSS_SELECTOR, ".dropdown-menu .dropdown-item")
        self.tag_item = (By.CSS_SELECTOR, ".list-genres span")
        self.category_checkbox = (By.CSS_SELECTOR, ".list-checkbox .form-check-label")
        self.search_button = (By.CSS_SELECTOR, "a.btn-filter")

    def open_page(self):
        logger.info(" Mở trang Tìm kiếm nâng cao...")
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        time.sleep(2)

    def select_sort(self, sort_text):
        logger.info(f" Chọn sắp xếp: {sort_text}")
        self.driver.find_element(*self.sort_dropdown).click()
        options = self.driver.find_elements(*self.sort_option)
        for opt in options:
            if sort_text.strip().lower() in opt.text.strip().lower():
                opt.click()
                logger.info(f" Đã chọn '{sort_text}'")
                return
        logger.warning(f" Không tìm thấy tùy chọn sắp xếp: {sort_text}")
        self.driver.find_element(By.TAG_NAME, "body").click()


    def select_category(self, category_name):
        logger.info(f" Chọn thể loại: {category_name}")
        cats = self.driver.find_elements(*self.category_checkbox)
        for c in cats:
            if c.text.strip().lower() == category_name.lower():
                c.click()
                return
        logger.warning(f" Không tìm thấy thể loại {category_name}")

    def select_tag(self, tag_name):
        logger.info(f" Chọn tag: {tag_name}")
        tags = self.driver.find_elements(*self.tag_item)
        for tag in tags:
            if tag.text.strip().lower() == tag_name.lower():
                self.driver.execute_script("arguments[0].scrollIntoView(true);", tag)
                ActionChains(self.driver).move_to_element(tag).click().perform()
                return
        logger.warning(f" Không tìm thấy tag {tag_name}")

    def click_search(self):
        logger.info(" Nhấn nút Tìm kiếm")
        btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.search_button)
        )
        btn.click()
        time.sleep(3)

    def verify_results_loaded(self):
        logger.info(" Kiểm tra kết quả hiển thị...")

        try:
            # Chờ phần thông báo kết quả xuất hiện
            result_info = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".group-title strong.color"))
            )
            result_count = result_info.text.strip()
            logger.info(f"  Trang đã hiển thị kết quả: Có {result_count} truyện liên quan.")
        except Exception:
            # Nếu không có thông báo kết quả -> thử kiểm tra danh sách truyện
            results = self.driver.find_elements(By.CSS_SELECTOR, ".series-item, .tab-content .result li")
            if len(results) > 0:
                logger.info(f"  Có {len(results)} truyện hiển thị (không có tổng số hiển thị).")
            else:
                logger.warning("  Không có kết quả nào hiển thị trên trang.")


    def close_browser(self):
        self.driver.quit()
        logger.info(" Đã đóng trình duyệt.")
