import sys, os
from selenium import webdriver
import pytest

# Thêm path để import module News.pages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from News.pages.news_page import NewsPage


@pytest.mark.news
def test_news_page_navigation():
    driver = webdriver.Chrome()
    driver.maximize_window()
    news = NewsPage(driver)

    try:
        print("\n Mở trang chủ...")
        news.open_homepage()

        print(" Click vào menu Tin tức...")
        news.click_news_menu()
        assert news.verify_news_page(), " Không vào đúng trang Tin tức!"

        print(" Mở bài viết đầu tiên...")
        news.open_first_news_item()
        assert news.verify_news_detail_page(), " Không mở đúng bài viết chi tiết!"

        print(" Test Tin tức chạy thành công!")

    finally:
        news.close_browser()
