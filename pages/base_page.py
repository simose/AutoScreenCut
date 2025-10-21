import os
import datetime
import time
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def maximize_window(self):
        # Playwright's default browser context usually starts with a maximized window
        # or adjusts to the viewport size set. To ensure full screen, we can set a large viewport.
        # However, a true 'maximize' button click isn't directly exposed. 
        # We'll set a common large resolution.
        self.page.set_viewport_size({"width": 1920, "height": 1080})

    def wait(self, seconds: int):
        self.page.wait_for_timeout(seconds * 1000)

    def close_popups(self):
        # This is a generic approach. Pop-ups can vary greatly.
        # We'll try to close common types of pop-ups like cookie banners or newsletters.
        # This might need to be extended based on specific website pop-ups.
        selectors = [
            'button:has-text("Close")',
            'button[aria-label="Close"]',
            'div[role="dialog"] button:has-text("No thanks")',
            '#onetrust-accept-btn-handler', # Common cookie consent button
            '.close-button',
            '.popup-close',
            '.modal-close'
        ]
        for selector in selectors:
            try:
                if self.page.locator(selector).is_visible():
                    self.page.locator(selector).click()
                    self.page.wait_for_timeout(500) # short wait for popup to disappear
            except Exception:
                pass

    def take_full_page_screenshots(self, url: str, output_dir: str, prefix_type: str):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get current date for folder naming
        today = datetime.date.today().strftime("%Y-%m-%d")
        screenshot_folder = os.path.join(output_dir, today)
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)

        # Generate prefix based on URL
        if "https://www.jackery.com/" == url:
            # For main page, use current date as prefix
            prefix = today.replace("-", "")
        else:
            # For other pages, extract meaningful name from URL
            url_parts = url.replace("https://www.jackery.com/", "").split("/")
            if url_parts[0]:
                prefix = url_parts[0].replace("-", "-")
            else:
                prefix = "jackery-page"

        # Cleanup existing screenshots for the same prefix and type to restart numbering
        try:
            for filename in os.listdir(screenshot_folder):
                if filename.startswith(f"{prefix}_{prefix_type}_") and filename.endswith(".png"):
                    file_path = os.path.join(screenshot_folder, filename)
                    os.remove(file_path)
            print(f"清理完成：已移除 {prefix}_{prefix_type}_*.png 旧文件")
        except Exception as e:
            print(f"清理旧文件时出错：{e}")

        screenshot_count = 1
        previous_scroll_position = -1
        current_scroll_position = 0

        while current_scroll_position != previous_scroll_position:
            # Scroll to the current position
            self.page.evaluate(f"window.scrollTo(0, {current_scroll_position})")
            self.page.wait_for_timeout(1000)  # Wait for scroll and content to load

            # Generate screenshot name with new format: prefix_A/B_001
            screenshot_name = f"{prefix}_{prefix_type}_{screenshot_count:03d}.png"
            screenshot_path = os.path.join(screenshot_folder, screenshot_name)
            self.page.screenshot(path=screenshot_path, full_page=False) # Take screenshot of visible part
            print(f"Screenshot saved: {screenshot_path}")

            previous_scroll_position = current_scroll_position
            # Scroll down to the next section
            current_scroll_position = self.page.evaluate("window.innerHeight + window.scrollY")
            
            # Check if we are at the bottom of the page
            page_height = self.page.evaluate("document.body.scrollHeight")
            if current_scroll_position >= page_height:
                current_scroll_position = page_height # Ensure we don't scroll past the end
                if previous_scroll_position == current_scroll_position:
                    break # Reached the bottom and no more scrolling possible
            
            screenshot_count += 1