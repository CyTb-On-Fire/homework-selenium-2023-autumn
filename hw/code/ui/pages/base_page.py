import time
from typing import List

import allure                                                                                                           # type: ignore
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from ui.locators import basic_locators
from ui.wait_conditions import element_in_viewport


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):

    locators = basic_locators.BasePageLocators()
    url = 'https://ads.vk.com/'

    def is_opened(self, timeout=15):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url.startswith(self.url):
                return True
        raise PageNotOpenedExeption(f'{self.url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def __init__(self, driver: RemoteWebDriver):
        self.driver = driver
        self.is_opened()

        self.close_cookie_banner()

    def close_cookie_banner(self):
        try:
            self.click(self.locators.COOKIE_BANNER_BUTTON)
        except:
            pass

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def is_visible(self, locator):
        elem = self.find(locator)
        elem.location_once_scrolled_into_view

    def is_not_visible(self, locator, timeout=None):
        self.wait(timeout).until(EC.invisibility_of_element(locator))

    def find(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_from(self, elem, locator, timeout=None):
        self.wait(timeout).until(lambda _: elem.find_element(*locator).is_displayed())

    def find_multiple(self, locator, timeout=None) -> List[WebElement]:
        return self.wait(timeout).until(EC.visibility_of_all_elements_located(locator))

    def switch_to_new_tab(self):
        assert len(self.driver.window_handles) > 1
        self.driver.switch_to.window(self.driver.window_handles[1])

    def switch_to_initial_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    @allure.step('Click')
    def click(self, locator, timeout=None) -> WebElement:
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()
        return elem

    @allure.step('Scroll click')
    def scroll_click(self, locator, timeout=None) -> WebElement:
        self.find(locator, timeout)

        self.wait(timeout).until(EC.visibility_of_element_located(locator))
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))

        elem.location_once_scrolled_into_view

        self.wait(timeout).until(element_in_viewport(locator))

        elem.click()

        return elem

    @allure.step('Fill in')
    def fill_in(self, locator, query, timeout=None) -> WebElement:
        elem = self.wait(timeout).until(EC.visibility_of_element_located(locator))
        elem.clear()
        elem.send_keys(query)
        return elem

    def get_selected_value(self, locator):
        select = Select(self.find(locator))
        return select.all_selected_options[0]

    def select_value(self, locator, value):
        select = Select(self.find(locator))
        select.select_by_visible_text(value)

    @allure.step('Check url')
    def assert_url(self, url, timeout=None):
        if timeout is None:
            timeout = 5
        try:
            self.wait(timeout).until(EC.url_matches(url))
        except:
            raise PageNotOpenedExeption(f'{url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def wait_for_redirect(self, timeout=None):
        self.wait(timeout).until(EC.url_changes(self.driver.current_url))
