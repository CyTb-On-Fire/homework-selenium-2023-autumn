import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.cases_page import CasesPage
from ui.pages.registration_page import RegistrationMainPage
from ui.pages.registration_page import RegistrationPage


@pytest.fixture()
def driver(config):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '118.0',
        }
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome()
    elif browser == 'firefox':
        driver = webdriver.Firefox()
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


def get_driver(browser_name):
    if browser_name == 'chrome':
        browser = webdriver.Chrome()
    elif browser_name == 'firefox':
        browser = webdriver.Firefox()
    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.maximize_window()
    return browser


@pytest.fixture(scope='session', params=['chrome', 'firefox'])
def all_drivers(config, request):
    url = config['url']
    browser = get_driver(request.param)
    browser.get(url)
    yield browser
    browser.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def cases_page(driver):
    driver.get(CasesPage.url)
    return CasesPage(driver=driver)


@pytest.fixture
def registration_main_page(driver):
    driver.get(RegistrationMainPage.url)
    return RegistrationMainPage(driver=driver)


@pytest.fixture(scope='session')
def account_selection_cookies(credentials, config):
    driver = get_driver(config['browser'])
    driver.get(RegistrationMainPage.url)

    page = RegistrationMainPage(driver)
    page.select_mail_account(*credentials)
    page.assert_url(RegistrationMainPage.url)
    driver.get(RegistrationPage.url)

    cookies = driver.get_cookies()

    driver.quit()
    return cookies


@pytest.fixture
def registration_page(driver):
    driver.get(RegistrationPage.url)
    # print("\nCookies got from fixture")
    # for cookie in account_selection_cookies:
    #     print(f"{cookie['name']} : {cookie['value']}")
    #     driver.add_cookie(cookie)

    # driver.refresh()
    return RegistrationPage(driver=driver)
