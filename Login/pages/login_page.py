from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Đăng nhập')]")
    GOOGLE_LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Đăng nhập với Google')]")
    EMAIL_FIELD = (By.ID, "identifierId")
    PASSWORD_FIELD = (By.NAME, "Passwd")
    NEXT_EMAIL_BUTTON = (By.ID, "identifierNext")
    NEXT_PASSWORD_BUTTON = (By.ID, "passwordNext")

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)

    def click_login(self):
        self.logger.info("Nhấn vào nút Đăng nhập")
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def click_login_with_google(self):
        self.logger.info("Nhấn vào nút 'Đăng nhập với Google'")
        self.wait.until(EC.element_to_be_clickable(self.GOOGLE_LOGIN_BUTTON)).click()

    def switch_to_google_popup(self):
        self.logger.info("Chuyển qua popup Google nếu có")
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if "accounts.google.com" in self.driver.current_url:
                return
        self.logger.warning("Không thấy popup Google, ở lại trang hiện tại")

    def enter_email(self, email):
        self.logger.info(f"Nhập email: {email}")
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(email)

    def click_next_email(self):
        self.logger.info("Nhấn Tiếp theo (sau email)")
        self.wait.until(EC.element_to_be_clickable(self.NEXT_EMAIL_BUTTON)).click()

    def enter_password(self, password):
        self.logger.info("Nhập mật khẩu")
        pwd_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        pwd_field.send_keys(password)

    def click_next_password(self):
        self.logger.info("Nhấn Tiếp theo (sau mật khẩu)")
        self.wait.until(EC.element_to_be_clickable(self.NEXT_PASSWORD_BUTTON)).click()
