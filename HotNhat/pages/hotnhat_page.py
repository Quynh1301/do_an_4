import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Logging cấu hình
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("artifacts/hotnhat_test.log", mode="w", encoding="utf-8")
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S")

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class HotNhatPage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://hangtruyen.top/"
        self.hotnhat_menu = (By.XPATH, "//ul[contains(@class,'main-menu')]//a[@href='/hot-nhat?type=all']")
        self.tab_all = (By.XPATH, "//a[contains(@href, 'hot-nhat?type=all')]")
        self.tab_day = (By.XPATH, "//a[contains(@href, 'hot-nhat?type=day')]")
        self.tab_week = (By.XPATH, "//a[contains(@href, 'hot-nhat?type=week')]")
        self.tab_month = (By.XPATH, "//a[contains(@href, 'hot-nhat?type=month')]")

    def open_homepage(self):
        logger.info(" Mở trang chủ...")
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        time.sleep(2)

    def click_hotnhat_menu(self):
        logger.info(" Click vào menu 'Hot nhất' ...")
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.hotnhat_menu)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)
        element.click()

    def click_tab(self, tab_locator, tab_name):
        logger.info(f" Click tab '{tab_name}' ...")
        try:
            tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(tab_locator)
            )
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(2)
            current_url = self.driver.current_url
            logger.info(f" URL sau khi click {tab_name}: {current_url}")
            return current_url
        except Exception as e:
            screenshot_path = f"artifacts/hotnhat_{tab_name}_fail.png"
            self.driver.save_screenshot(screenshot_path)
            logger.error(f" Lỗi khi click {tab_name}: {e}. Ảnh: {screenshot_path}")
            raise

    def close_browser(self):
        self.driver.quit()
        logger.info(" Đã đóng trình duyệt.")
