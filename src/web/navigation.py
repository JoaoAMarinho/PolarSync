from utils.logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .constants import LOGIN_URL, TRAINING_DATE_URL


def login(driver, config):
    """
    Login to Polar Flow using the provided credentials.
    """
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
    )

    driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(
        config["username"]
    )
    driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(
        config["username"], Keys.RETURN
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//h1[contains(text(), "You are signed in to Polar services")]')
        )
    )
    logger.info("Login successful!")


def accept_cookies(driver, session):
    """
    Accept necessary cookies in the Polar Flow website.
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection",
                )
            )
        )
        cookie_button = driver.find_element(
            By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"
        )
        cookie_button.click()

        def set_cookies(session, cookies):
            for cookie in cookies:
                session.cookies.set(cookie["name"], cookie["value"])

        set_cookies(session, driver.get_cookies())
    except Exception as e:
        logger.error("Cookie consent button not found or already accepted:", e)


def navigate_to_workout_page(driver):
    driver.get(TRAINING_DATE_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//h1[contains(text(), "Adicionar objetivo de treino")]')
        )
    )
    print("Navigated to training objective page.")
