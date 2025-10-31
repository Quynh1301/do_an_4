import os
from datetime import datetime

def take_screenshot(driver, name):
    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f" Screenshot saved: {path}")
