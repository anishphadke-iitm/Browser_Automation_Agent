from playwright.sync_api import sync_playwright
import time


class BrowserController:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=True
        )

        self.page = self.browser.new_page()

        # Popup handler
        self.page.on(
            "dialog",
            self.handle_dialog
        )

    def handle_dialog(self, dialog):
        print("Popup detected:", dialog.message)
        dialog.accept()

    # Retry helper
    def retry_action(self, func, *args):

        retries = 3

        for attempt in range(retries):

            try:
                return func(*args)

            except Exception as e:

                print(
                    f"Retry {attempt + 1} failed:",
                    e
                )

                time.sleep(2)

        print("Action failed after retries.")

    def navigate(self, url):
        print(f"Navigating to {url}")

        self.retry_action(
            self.page.goto,
            url
        )

    def click(self, selector):
        print(f"Clicking {selector}")

        self.retry_action(
            self.page.click,
            selector
        )

    def fill(self, selector, text):
        print(f"Filling {selector}")

        self.retry_action(
            self.page.fill,
            selector,
            text
        )

    def extract(self, selector):
        print(f"Extracting {selector}")

        text = self.retry_action(
            self.page.inner_text,
            selector
        )

        print("Extracted:", text)

        return text

    def wait(self, seconds):
        print(f"Waiting {seconds} seconds")

        self.page.wait_for_timeout(
            seconds * 1000
        )

    def close(self):
        self.browser.close()
        self.playwright.stop()