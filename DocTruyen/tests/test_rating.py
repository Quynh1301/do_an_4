import pytest
import time
from selenium import webdriver
from DocTruyen.pages.rating_page import RatingPage
from DocTruyen.utils.logger import get_logger
from DocTruyen.utils.screenshot_helper import take_screenshot

def test_rating_story():
    driver = webdriver.Chrome()
    driver.maximize_window()
    logger = get_logger("TestRating")

    rating_page = RatingPage(driver, logger)

    try:
        # 1️ Đăng nhập
        rating_page.login("qbui14494@gmail.com", "zxCvBNma577@")

        # 2️ Mở truyện đầu tiên
        rating_page.open_first_story()

        # 3️ Thực hiện đánh giá (ví dụ: TUYỆT VỜI)
        rating_page.rate_story("TUYỆT VỜI")

        logger.info(" Test đánh giá truyện hoàn tất!")

    except Exception as e:
        screenshot = take_screenshot(driver, "rating_error")
        logger.error(f" Lỗi: {e}")
        logger.error(f"Ảnh lỗi: {screenshot}")
        pytest.fail(str(e))

    finally:
        time.sleep(2)
        driver.quit()
