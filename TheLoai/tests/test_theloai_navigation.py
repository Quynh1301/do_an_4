import sys, os, pytest, logging
from selenium import webdriver

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from TheLoai.pages.theloai_page import TheLoaiPage

logger = logging.getLogger(__name__)

@pytest.mark.theloai
def test_theloai_navigation():
    """Kiểm thử menu Thể loại và các thể loại con"""
    driver = webdriver.Chrome()
    theloai = TheLoaiPage(driver)

    try:
        logger.info("\n=== BẮT ĐẦU KIỂM THỬ THỂ LOẠI ===")
        theloai.open_homepage()
        theloai.hover_menu()  

        urls = {
            "Manga": theloai.click_category(theloai.manga, "Manga"),
            "Manhua": theloai.click_category(theloai.manhua, "Manhua"),
            "Manhwa": theloai.click_category(theloai.manhwa, "Manhwa"),
            "Marvel": theloai.click_category(theloai.marvel, "Marvel Comics"),
            "DC": theloai.click_category(theloai.dc, "DC Comics")
        }

        #  Kiểm tra URL đúng
        assert "the-loai/manga" in urls["Manga"], " Manga sai link!"
        assert "the-loai/manhua" in urls["Manhua"], " Manhua sai link!"
        assert "the-loai/manhwa" in urls["Manhwa"], " Manhwa sai link!"
        assert "the-loai/marvel-comics" in urls["Marvel"], " Marvel Comics sai link!"
        assert "the-loai/dc-comics" in urls["DC"], " DC Comics sai link!"

        logger.info("  Tất cả thể loại hiển thị đúng URL!")

    finally:
        theloai.close_browser()
        logger.info(" Kết thúc kiểm thử Thể loại.")
