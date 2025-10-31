import pytest
from DocTruyen.pages.read_page import ReadPage
from DocTruyen.utils.logger import get_logger
from DocTruyen.utils.screenshot_helper import take_screenshot
from selenium import webdriver

def test_read_story_from_home():
    logger = get_logger("ReadFromHome")
    driver = webdriver.Chrome()
    driver.maximize_window()
    read_page = ReadPage(driver, logger)

    try:
        # 1️ Mở trang chủ
        read_page.open_homepage()

        # 2️ Cuộn xuống và click truyện đầu tiên
        read_page.scroll_to_stories()
        story_name = read_page.click_first_story()

        # 3️ Kiểm tra vào đúng truyện
        read_page.verify_story_opened(story_name)

        # 4️ Nhấn “Đọc ngay”
        read_page.click_read_now()

        # 5️ Kiểm tra đã vào trang đọc chương
        read_page.verify_chapter_loaded()

        # 6️ Cài đặt đọc (tùy chọn)
        read_page.open_setting_panel()
        read_page.change_read_mode()
        read_page.change_zoom_mode()
        read_page.switch_dark_mode()

        # 7️ Báo lỗi (tùy chọn)
        read_page.open_report_form()
        read_page.send_report("Ảnh bị lỗi hoặc chap bị trùng")

    except Exception as e:
        screenshot = take_screenshot(driver, "read_from_home_error")
        logger.error(f" Lỗi: {e}")
        logger.error(f"Ảnh lỗi: {screenshot}")
        pytest.fail(str(e))
    finally:
        driver.quit()
