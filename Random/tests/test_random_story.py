import sys, os, time, pytest
from selenium import webdriver

# Thêm path để import module Random.pages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Random.pages.random_page import RandomPage


@pytest.mark.random
def test_random_story_navigation():
    """Kiểm thử tính năng Random truyện (1 lần)"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    random_page = RandomPage(driver)

    try:
        print("\n=== BẮT ĐẦU KIỂM THỬ RANDOM TRUYỆN ===")
        random_page.open_homepage()

        random_page.click_random_story()
        time.sleep(3)

        current_url = random_page.get_current_story_url()
        assert "https://hangtruyen.org/truyen-tranh/" in current_url, \
            " Không mở đúng trang truyện sau khi random!"
        print("  Random mở đúng trang truyện thành công!")

    finally:
        random_page.close_browser()
