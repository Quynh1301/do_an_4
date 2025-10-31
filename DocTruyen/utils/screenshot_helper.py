import os
from datetime import datetime

def take_screenshot(driver, name="error"):
    screenshot_dir = os.path.join("artifacts", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    return file_path
