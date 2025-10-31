import sys, os, pytest, logging
from selenium import webdriver

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Tags.pages.tags_page import TagsPage

logger = logging.getLogger(__name__)

@pytest.mark.tags
def test_tags_navigation():
    """Kiểm thử menu Tags và các tag con"""
    driver = webdriver.Chrome()
    tags = TagsPage(driver)

    try:
        logger.info("\n=== BẮT ĐẦU KIỂM THỬ TAGS ===")
        tags.open_homepage()
        tags.hover_menu_tag()

        urls = {
            "HangTruyen": tags.click_tag(tags.hangtruyen, "HangTruyen"),
            "Action": tags.click_tag(tags.action, "Action"),
            "Romance": tags.click_tag(tags.romance, "Romance"),
        }

        # Kiểm tra URL đúng
        assert "genre/hangtruyen" in urls["HangTruyen"], " HangTruyen sai link!"
        assert "genre/action" in urls["Action"], " Action sai link!"
        assert "genre/romance" in urls["Romance"], " Romance sai link!"

        logger.info("  Tất cả tag hiển thị đúng URL!")

    finally:
        tags.close_browser()
        logger.info(" Kết thúc kiểm thử Tags.")
