import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Cấu hình log ghi file + hiển thị ra console
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Ghi log vào file artifacts/random_test.log
file_handler = logging.FileHandler("artifacts/random_test.log", mode="w", encoding="utf-8")
console_handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class RandomPage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://hangtruyen.top/"
        self.random_link = (By.XPATH, "//ul[contains(@class,'main-menu')]//a[@href='/random']")

    def open_homepage(self):
        logger.info(" Mở trang chủ...")
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        time.sleep(2)

    def click_random_story(self):
        logger.info(" Đang tìm và nhấn nút Random...")
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.random_link)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.random_link)
                ).click()
                logger.info(" Đã click nút Random bằng Selenium click().")
            except Exception:
                self.driver.execute_script("arguments[0].click();", element)
                logger.warning(" Đã click nút Random bằng JavaScript fallback.")
        except Exception as e:
            screenshot_path = "artifacts/random_fail.png"
            self.driver.save_screenshot(screenshot_path)
            logger.error(f" Lỗi khi click Random: {e}. Đã chụp ảnh: {screenshot_path}")
            raise

    def get_current_story_url(self):
        current_url = self.driver.current_url
        logger.info(f"🔗 URL hiện tại: {current_url}")
        return current_url

    def close_browser(self):
        self.driver.quit()
        logger.info(" Đã đóng trình duyệt.")
