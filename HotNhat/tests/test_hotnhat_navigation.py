import sys, os, pytest, logging, time
from selenium import webdriver

# Thêm path để import module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from HotNhat.pages.hotnhat_page import HotNhatPage

logger = logging.getLogger(__name__)

@pytest.mark.hotnhat
def test_hotnhat_tabs_navigation():
    """Kiểm thử 4 tab 'Hot nhất': All, Day, Week, Month"""
    driver = webdriver.Chrome()
    hotnhat_page = HotNhatPage(driver)

    try:
        logger.info("\n=== BẮT ĐẦU KIỂM THỬ HOT NHẤT ===")
        hotnhat_page.open_homepage()
        hotnhat_page.click_hotnhat_menu()

        #  Kiểm thử từng tab
        urls = {
            "All": hotnhat_page.click_tab(hotnhat_page.tab_all, "All"),
            "Day": hotnhat_page.click_tab(hotnhat_page.tab_day, "Day"),
            "Week": hotnhat_page.click_tab(hotnhat_page.tab_week, "Week"),
            "Month": hotnhat_page.click_tab(hotnhat_page.tab_month, "Month")
        }

        #  Kiểm tra URL đúng kỳ vọng
        assert "hot-nhat?type=all" in urls["All"], " Tab All sai link!"
        assert "hot-nhat?type=day" in urls["Day"], " Tab Day sai link!"
        assert "hot-nhat?type=week" in urls["Week"], " Tab Week sai link!"
        assert "hot-nhat?type=month" in urls["Month"], " Tab Month sai link!"

        logger.info(" Tất cả tab Hot nhất hiển thị đúng URL!")

    finally:
        hotnhat_page.close_browser()
        logger.info(" Kết thúc kiểm thử Hot nhất.")
