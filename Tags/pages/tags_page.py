import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# Thiết lập logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("artifacts/tags_test.log", mode="w", encoding="utf-8")
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class TagsPage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://hangtruyen.top/"

        # Menu chính
        self.menu_tag = (By.XPATH, "//a[@href='/genre' and contains(@class, 'sub-toggle')]")

        # Các tag con
        self.hangtruyen = (By.XPATH, "//a[@href='/genre/hangtruyen']")
        self.action = (By.XPATH, "//a[@href='/genre/action']")
        self.romance = (By.XPATH, "//a[@href='/genre/romance']")

    def open_homepage(self):
        logger.info(" Mở trang chủ...")
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        time.sleep(2)

    def hover_menu_tag(self):
        """Di chuột mở menu 'Tags' để hiển thị dropdown"""
        logger.info(" Di chuột mở menu 'Tags'...")
        menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.menu_tag)
        )
        ActionChains(self.driver).move_to_element(menu).perform()
        time.sleep(1)

    def click_tag(self, locator, name):
        """Click vào từng tag cụ thể"""
        logger.info(f" Click vào tag '{name}' ...")
        try:
            # Hover lại menu mỗi lần click
            self.hover_menu_tag()

            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(2)
            current_url = self.driver.current_url
            logger.info(f"  URL sau khi click {name}: {current_url}")
            return current_url

        except Exception as e:
            screenshot = f"artifacts/tags_{name}_error.png"
            self.driver.save_screenshot(screenshot)
            logger.error(f"  Lỗi khi click {name}: {e}. Ảnh: {screenshot}")
            raise

    def close_browser(self):
        self.driver.quit()
        logger.info(" Đã đóng trình duyệt.")
