from utils.logger import logger
from datetime import datetime
from .constants import LOGIN_URL, DIARY_URL, TRAINING_DATE_URL


def login(browser, config):
    """
    Log in to the Polar Flow website using config values.
    """
    browser.goto(LOGIN_URL)

    # Fill in the username and password
    browser.fill('input[name="username"]', config["username"])
    browser.fill('input[name="password"]', config["password"])
    browser.click('button[type="submit"]')

    if browser.url.endswith("/login"):
        raise Exception("Login failed or page did not redirect correctly.")

    # Click the login button
    logger.info("Login successful!")


def accept_cookies(browser, session):
    """
    Accept necessary cookies.
    """
    try:
        button = browser.locator(
            "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"
        )
        button.click()

        def set_cookies(session, cookies):
            for cookie in cookies:
                session.cookies.set(cookie["name"], cookie["value"])
            session.cookies.set("timezone", "0")

        set_cookies(session, browser.context.cookies())
    except Exception as e:
        logger.error("Cookie consent button not found or already accepted:", e)


def navigate_to_objective_target(browser, objective):
    """
    Navigate to the objective target page.
    """
    formated_date = datetime.fromisoformat(objective["datetime"]).strftime("%Y-%m-%d")
    browser.goto(TRAINING_DATE_URL + formated_date)
    logger.info(f"Navigated to '{formated_date}' objective target page.")


def navigate_to_diary(browser):
    """
    Navigate to the diary page.
    """
    browser.goto(DIARY_URL)
    logger.info("Navigated to diary page.")
