from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime


class BrowserController:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=True
        )

        self.page = self.browser.new_page()

        # Create folders if missing
        os.makedirs("logs", exist_ok=True)
        os.makedirs("screenshots", exist_ok=True)

        # Popup handler
        self.page.on(
            "dialog",
            self.handle_dialog
        )

    def log(self, message):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_message = f"[{timestamp}] {message}"

        print(log_message)

        with open("logs/agent.log", "a") as f:
            f.write(log_message + "\n")

    def screenshot(self, name):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = f"screenshots/{name}_{timestamp}.png"

        self.page.screenshot(
            path=filename
        )

        self.log(f"Screenshot saved: {filename}")

    def handle_dialog(self, dialog):

        self.log(
            f"Popup detected: {dialog.message}"
        )

        dialog.accept()

    def retry_action(self, func, *args):

        retries = 3
        last_error = None

        for attempt in range(retries):

            try:

                return func(*args)

            except Exception as e:

                last_error = e

                self.log(
                    f"Retry {attempt + 1}/{retries} failed: {e}"
                )

                time.sleep(2)

        self.screenshot("failure")

        raise RuntimeError(
            f"Action failed after {retries} retries: {last_error}"
        )

    def navigate(self, url):

        self.log(f"Navigating to {url}")

        self.retry_action(
            self.page.goto,
            url
        )

        self.page.wait_for_timeout(2000)

        self.screenshot("after_navigation")

    def click(self, selector):

        self.log(f"Clicking {selector}")

        self.retry_action(
            self.page.click,
            selector
        )

        self.page.wait_for_timeout(2000)

        self.screenshot("after_click")

    def fill(self, selector, text):

        self.log(f"Filling {selector}")

        self.retry_action(
            self.page.fill,
            selector,
            text
        )

        self.page.wait_for_timeout(1000)

        self.screenshot("after_fill")

    def extract(self, selector):

        self.log(f"Extracting {selector}")

        self.page.wait_for_timeout(2000)

        text = self.retry_action(
            self.page.inner_text,
            selector
        )

        self.log(f"Extracted: {text}")

        self.screenshot("after_extract")

        return text

    def wait(self, seconds):

        self.log(f"Waiting {seconds} seconds")

        self.page.wait_for_timeout(
            seconds * 1000
        )

    def close(self):

        self.screenshot("final")

        self.browser.close()

        self.playwright.stop()