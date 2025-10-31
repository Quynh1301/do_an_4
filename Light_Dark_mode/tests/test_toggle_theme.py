import sys, os, time, pytest
from selenium import webdriver

# Thêm path để import module Light_Dark_mode.pages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Light_Dark_mode.pages.theme_page import ThemePage


@pytest.mark.light_dark
def test_toggle_dark_and_light_mode():
    driver = webdriver.Chrome()
    driver.maximize_window()
    page = ThemePage(driver)

    try:
        print("\n=== BẮT ĐẦU KIỂM THỬ DARK/LIGHT MODE ===")
        page.open_page("https://hangtruyen.top/")
        print(" Đã mở trang chủ thành công")

        # Lấy màu nền trước
        color_before = page.get_background_color()
        print(f" Màu nền trước khi đổi: {color_before}")

        # Click chuyển đổi
        print(" Thực hiện đổi giao diện Light/Dark...")
        page.click_toggle_mode()
        time.sleep(2)

        # Lấy màu nền sau
        color_after = page.get_background_color()
        print(f" Màu nền sau khi đổi: {color_after}")

        # So sánh kết quả
        assert color_before != color_after, " Nền không thay đổi sau khi click!"
        print(" Giao diện Light/Dark thay đổi thành công!")

    finally:
        page.close_browser()
        print(" Đã đóng trình duyệt.")

