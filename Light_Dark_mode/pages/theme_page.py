from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ThemePage:
    def __init__(self, driver):
        self.driver = driver
        self.toggle_button = (By.CSS_SELECTOR, ".dark-mode button.btn-switch")

    def open_page(self, url):
        """Mở trang web"""
        self.driver.get(url)

    def click_toggle_mode(self):
        """Click nút chuyển đổi giao diện Light/Dark"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.toggle_button)
        )
        button.click()

    def get_background_color(self):
        """Lấy màu nền hiện tại"""
        body = self.driver.find_element(By.TAG_NAME, "body")
        return body.value_of_css_property("background-color")

    def close_browser(self):
        """Đóng trình duyệt"""
        self.driver.quit()
