import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewsPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://hangtruyen.top/"
        self.menu_news = (By.XPATH, "//a[contains(@href,'/tin-tuc')]")
        self.first_news_item = (By.XPATH, "(//div[@class='single-item']//a)[1]")

        #  Cấu hình logger
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.FileHandler("artifacts/logs/news_log.txt", mode='w', encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def open_homepage(self):
        self.logger.info(" Mở trang chủ: %s", self.url)
        self.driver.get(self.url)

    def click_news_menu(self):
        self.logger.info(" Click vào menu Tin tức...")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.menu_news)
        ).click()

    def verify_news_page(self):
        self.logger.info(" Kiểm tra URL có chứa '/tin-tuc' ...")
        current_url = self.driver.current_url
        result = "/tin-tuc" in current_url
        self.logger.info(" Kết quả: %s", result)
        return result

    def open_first_news_item(self):
        self.logger.info(" Mở bài viết đầu tiên...")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.first_news_item)
        ).click()

    def verify_news_detail_page(self):
        self.logger.info(" Kiểm tra trang chi tiết bài viết...")
        current_url = self.driver.current_url
        result = "/tin-tuc/" in current_url
        self.logger.info(" Kết quả: %s", result)
        return result

    def close_browser(self):
        self.logger.info(" Đóng trình duyệt.")
        self.driver.quit()
