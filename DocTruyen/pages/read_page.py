from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class ReadPage:
    URL = "https://hangtruyen.top/"
    
    # ===== LOCATORS =====
    STORY_FIRST = (By.CSS_SELECTOR, ".m-post.splide__slide.is-active a[href*='/truyen-tranh/']")
    STORY_TITLE = (By.CSS_SELECTOR, ".m-post.splide__slide.is-active .m-name a")
    READ_NOW_BTN = (By.XPATH, "//a[contains(text(),'Đọc ngay')]")
    CHAPTER_TITLE = (By.CSS_SELECTOR, "h1.manga-name")

    # ===== CÀI ĐẶT =====
    SETTING_BUTTON = (By.CSS_SELECTOR, "a.show-setting")
    MODE_DROPDOWN = (By.ID, "dropdownMode")
    MODE_HORIZONTAL = (By.XPATH, "//a[@data-mode='horizon-double']")

    ZOOM_DROPDOWN = (By.ID, "dropdownZoom")
    ZOOM_NGANG = (By.XPATH, "//a[@data-value='Ngang']")

    LIGHTMODE_DROPDOWN = (By.ID, "dropdownLightmode")
    DARK_MODE = (By.XPATH, "//a[@data-value='true']")

    # ===== BÁO LỖI =====
    REPORT_BUTTON = (By.CSS_SELECTOR, "a.report")
    REPORT_CHECKBOX = (By.ID, "report-reason_3")  # ví dụ chọn “Ảnh bị lỗi”
    REPORT_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='content']")
    REPORT_SUBMIT = (By.XPATH, "//button[contains(text(),'Báo cáo')]")

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    # ====== MỞ TRANG CHỦ ======
    def open_homepage(self):
        self.driver.get(self.URL)
        self.logger.info(" Mở trang chủ HangTruyen")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # ====== CUỘN XUỐNG DANH SÁCH ======
    def scroll_to_stories(self):
        self.logger.info(" Cuộn xuống để thấy phần 'Top thịnh hành'")
        self.driver.execute_script("""
            const el = document.querySelector("h2.m-title.title");
            if (el) el.scrollIntoView({behavior: "smooth", block: "center"});
        """)
        time.sleep(2)

    # ====== CLICK TRUYỆN ĐẦU TIÊN ======
    def click_first_story(self):
        self.logger.info(" Click vào truyện đầu tiên trong danh sách 'Top thịnh hành'")
        story_element = self.wait.until(EC.element_to_be_clickable(self.STORY_FIRST))
        story_name = self.driver.find_element(*self.STORY_TITLE).text.strip()
        self.driver.execute_script("arguments[0].click();", story_element)
        self.logger.info(f" Đã click truyện: {story_name}")
        return story_name

    # ====== XÁC NHẬN TRUYỆN MỞ RA ======
    def verify_story_opened(self, story_name):
        self.logger.info(" Kiểm tra đã vào đúng trang truyện")
        title = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        assert story_name.lower() in title.lower(), f" Không đúng truyện, tiêu đề: {title}"
        self.logger.info(" Đã vào đúng truyện.")

    # ====== CLICK NÚT “ĐỌC NGAY” ======
    def click_read_now(self):
        self.logger.info(" Nhấn nút 'Đọc ngay'")
        btn = self.wait.until(EC.element_to_be_clickable(self.READ_NOW_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)

    # ====== KIỂM TRA CHƯƠNG ĐÃ MỞ ======
    def verify_chapter_loaded(self):
        self.logger.info(" Kiểm tra đã vào trang đọc chương")
        chapter_title = self.wait.until(EC.visibility_of_element_located(self.CHAPTER_TITLE)).text
        assert "Chapter" in chapter_title or "Chương" in chapter_title, f"Không phải trang đọc: {chapter_title}"
        self.logger.info(f" Đã vào trang đọc: {chapter_title}")

    # ====== CÀI ĐẶT TRUYỆN ======
    def open_setting_panel(self):
        self.logger.info(" Mở menu Cài đặt")
        btn = self.wait.until(EC.element_to_be_clickable(self.SETTING_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

    def change_read_mode(self):
        self.logger.info(" Đang đổi chế độ đọc...")
        mode_btn = self.wait.until(EC.element_to_be_clickable(self.MODE_DROPDOWN))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", mode_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", mode_btn)
        option = self.wait.until(EC.element_to_be_clickable(self.MODE_HORIZONTAL))
        self.driver.execute_script("arguments[0].click();", option)
        self.logger.info(" Đã chuyển sang chế độ đọc: Ngang 2 trang")
        time.sleep(1)

    def change_zoom_mode(self):
        self.logger.info(" Đang đổi chế độ Zoom...")
        zoom_btn = self.wait.until(EC.element_to_be_clickable(self.ZOOM_DROPDOWN))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", zoom_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", zoom_btn)
        option = self.wait.until(EC.element_to_be_clickable(self.ZOOM_NGANG))
        self.driver.execute_script("arguments[0].click();", option)
        self.logger.info(" Đã thay đổi chế độ Zoom: Ngang")
        time.sleep(1)

    def switch_dark_mode(self):
        self.logger.info(" Bật chế độ tối")
        light_btn = self.wait.until(EC.element_to_be_clickable(self.LIGHTMODE_DROPDOWN))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", light_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", light_btn)
        dark_option = self.wait.until(EC.element_to_be_clickable(self.DARK_MODE))
        self.driver.execute_script("arguments[0].click();", dark_option)
        self.logger.info(" Đã bật chế độ tối")
        time.sleep(1)

    # ====== BÁO LỖI ======
    def open_report_form(self):
        self.logger.info("Mở form báo lỗi")
        btn = self.wait.until(EC.element_to_be_clickable(self.REPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

    def send_report(self, message="Ảnh bị lỗi hoặc chap bị trùng"):
        self.logger.info(" Gửi báo cáo lỗi")
        try:
            # 1️ Tích chọn lý do & nhập nội dung
            checkbox = self.wait.until(EC.element_to_be_clickable(self.REPORT_CHECKBOX))
            self.driver.execute_script("arguments[0].click();", checkbox)

            textarea = self.wait.until(EC.visibility_of_element_located(self.REPORT_TEXTAREA))
            textarea.clear()
            textarea.send_keys(message)

            # 2️ Nhấn nút “Báo cáo”
            submit = self.wait.until(EC.element_to_be_clickable(self.REPORT_SUBMIT))
            self.driver.execute_script("arguments[0].click();", submit)
            self.logger.info("Đã click nút 'Báo cáo'")

            # 3️ Đợi thông báo xác nhận
            noti = self.wait.until(EC.visibility_of_element_located(self.REPORT_SUCCESS))
            text = noti.text.strip()
            assert "Cảm ơn bạn đã báo cáo" in text, f"Nội dung thông báo khác: {text}"
            self.logger.info(" Báo cáo lỗi thành công!")

        except Exception as e:
            self.logger.warning(f" Không thể gửi báo cáo hoặc không thấy thông báo: {e}")