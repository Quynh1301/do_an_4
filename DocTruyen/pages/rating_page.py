from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class RatingPage:
    URL = "https://hangtruyen.top/"

    # ===== LOGIN LOCATORS =====
    LOGIN_BTN = (By.XPATH, "//span[contains(text(),'Đăng nhập')]")
    LOGIN_MODAL = (By.ID, "login-modal")  # popup đăng nhập
    EMAIL_TAB = (By.XPATH, "//a[contains(@href,'#tab-login-email')]")
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    SUBMIT_LOGIN = (By.XPATH, "//button[contains(text(),'Đăng nhập')]")

    # ===== TRUYỆN =====
    FIRST_STORY = (By.CSS_SELECTOR, ".m-post.splide__slide.is-active a[href*='/truyen-tranh/']")
    STORY_TITLE = (By.CSS_SELECTOR, ".m-post.splide__slide.is-active .m-name a")
    STORY_H1 = (By.TAG_NAME, "h1")

    # ===== ĐÁNH GIÁ =====
    RATE_BAD = (By.XPATH, "//*[name()='path' and contains(@d,'M38.7487 3')]")           # TỆ
    RATE_SOSO = (By.XPATH, "//*[name()='path' and contains(@d,'M39.1273 3')]")          # HƠI TỆ
    RATE_NORMAL = (By.XPATH, "//*[name()='path' and contains(@d,'M24.1477 3')]")        # BÌNH THƯỜNG
    RATE_GOOD = (By.XPATH, "//a[normalize-space()='Hay']//*[name()='path' and contains(@d,'M41.2034 5')]")  # HAY
    RATE_GREAT = (By.XPATH, "//*[name()='path' and contains(@d,'M21.7692 1')]")         # TUYỆT VỜI
    NOTI_RATED = (By.ID, "vote_noti")

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 20)
        self.actions = ActionChains(driver)

    # ====== ĐĂNG NHẬP ======
    def login(self, email, password):
        self.driver.get(self.URL)
        self.logger.info("Mở trang chủ HangTruyen")

        # Mở popup đăng nhập
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()
        self.logger.info("Đã click mở popup đăng nhập")

        # Chờ popup hiển thị
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_MODAL))

        # Chọn tab đăng nhập bằng email (nếu có tab Google và Email)
        try:
            self.wait.until(EC.element_to_be_clickable(self.EMAIL_TAB)).click()
            self.logger.info("Chuyển sang tab đăng nhập bằng Email")
        except:
            self.logger.warning("Không thấy tab đăng nhập email — có thể popup chỉ có 1 form duy nhất.")

        # Điền thông tin đăng nhập
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        pwd_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        email_field.clear()
        pwd_field.clear()
        email_field.send_keys(email)
        pwd_field.send_keys(password)

        # Nhấn nút đăng nhập
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_LOGIN)).click()
        self.logger.info("Đã nhấn nút Đăng nhập")

        # Chờ popup biến mất (đăng nhập thành công)
        time.sleep(2)
        self.wait.until_not(EC.visibility_of_element_located(self.LOGIN_MODAL))
        self.logger.info("Đăng nhập thành công!")

    # ====== MỞ TRUYỆN ======
    def open_first_story(self):
        self.logger.info("Mở truyện đầu tiên trong danh sách")
        self.wait.until(EC.element_to_be_clickable(self.FIRST_STORY)).click()
        title = self.wait.until(EC.visibility_of_element_located(self.STORY_H1)).text
        self.logger.info(f"Đã mở truyện: {title}")
        return title

    # ====== ĐÁNH GIÁ ======
    def rate_story(self, level="TUYỆT VỜI"):
        self.logger.info(f"Bắt đầu đánh giá truyện: {level}")

        level_map = {
            "TỆ": self.RATE_BAD,
            "HƠI TỆ": self.RATE_SOSO,
            "BÌNH THƯỜNG": self.RATE_NORMAL,
            "HAY": self.RATE_GOOD,
            "TUYỆT VỜI": self.RATE_GREAT
        }

        locator = level_map.get(level.upper(), self.RATE_GREAT)
        rate_button = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rate_button)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", rate_button)
        self.logger.info(f"Đã click đánh giá '{level}'")

        # Kiểm tra thông báo cảm ơn
        self.wait.until(EC.visibility_of_element_located(self.NOTI_RATED))
        noti_text = self.driver.find_element(*self.NOTI_RATED).text
        assert "Cảm ơn bạn" in noti_text, "Không thấy thông báo đánh giá!"
        self.logger.info("Hiển thị thông báo xác nhận đánh giá.")
