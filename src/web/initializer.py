from playwright.sync_api import sync_playwright


def initialize_browser(background=False):
    """
    Initialize Playwright and return a browser instance.
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=background
    )  # Set headless=True for background execution
    return browser.new_page()
