from selenium import webdriver


def initialize_driver():
    return webdriver.Chrome()


def close_driver(driver):
    driver.quit()
