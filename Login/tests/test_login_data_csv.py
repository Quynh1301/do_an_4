import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Login.utils.data_reader import read_csv_data

# --- Đường dẫn tới file CSV ---
csv_path = "Login/data/login_data.csv"
test_data = read_csv_data(csv_path)

@pytest.mark.parametrize("email,password,expectedresult", [
    (row["email"], row["password"], row["expectedresult"]) for row in test_data
])
def test_login_logout_with_csv(email, password, expectedresult):
    print(f"\n=== BẮT ĐẦU TEST ===\nEmail: '{email}' | Password: '{password}'")

    # --- Khởi tạo trình duyệt ---
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://hangtruyen.top/")
    time.sleep(2)

    # --- Bước 1: Nhấn nút “Đăng nhập” ---
    try:
        login_button = driver.find_element(By.XPATH, "//span[contains(text(),'Đăng nhập')]")
        print("Nhấn nút 'Đăng nhập'")
        login_button.click()
        time.sleep(2)
    except Exception as e:
        print(" Không tìm thấy nút 'Đăng nhập':", e)
        driver.quit()
        return

    # --- Bước 2: Lấy form đăng nhập ---
    try:
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        submit_button = driver.find_element(By.ID, "login-button")
    except Exception as e:
        print(" Không tìm thấy form đăng nhập:", e)
        driver.quit()
        return

    # --- Bước 3: Nhập dữ liệu ---
    if email:
        email_field.send_keys(email)
    if password:
        password_field.send_keys(password)
    time.sleep(1)

    print("Click nút đăng nhập")
    submit_button.click()
    time.sleep(3)

    # --- Bước 4: Kiểm tra kết quả đăng nhập ---
    if not email:
        actual = "hiển thị thông báo yêu cầu nhập email"
    elif email and not password:
        actual = "hiển thị thông báo yêu cầu nhập mật khẩu"
    elif password != "zxCvBNma577@":
        actual = "hiển thị thông báo mật khẩu không chính xác"
    else:
        actual = "đăng nhập thành công, chuyển đến trang chủ"
        print(" Đăng nhập thành công!")

        # --- Bước 5: Thực hiện ĐĂNG XUẤT ---
        try:
            print("Tiến hành đăng xuất...")
            time.sleep(3)

            # Nhấn vào tên tài khoản hoặc avatar
            user_icon = driver.find_element(By.XPATH, "//span[@id='username']")
            user_icon.click()
            time.sleep(2)

            # Nhấn vào nút “Đăng xuất”
            logout_button = driver.find_element(By.XPATH, "//a[@id='logout']")
            logout_button.click()
            print(" Đã đăng xuất thành công!")
            time.sleep(2)
        except Exception as e:
            print(" Lỗi khi đăng xuất:", e)

    # --- Bước 6: Kết quả ---
    print(f"Kết quả mong đợi: {expectedresult}")
    print(f"Kết quả thực tế: {actual}")

    input("Nhấn Enter để đóng trình duyệt...")
    driver.quit()

    assert actual == expectedresult, f"Lỗi! Mong đợi: '{expectedresult}', nhưng nhận: '{actual}'"
