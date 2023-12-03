class element_stops_moving:
    def __init__(self, locator):
        self.locator = locator
        self.prev_pos = {'x': -1, 'y': -1}

    def __call__(self, driver):
        elem = driver.find_element(*self.locator)
        res = elem.location == self.prev_pos
        self.prev_pos = elem.location

        if res:
            return elem
        return False


class element_visible_and_static:
    def __init__(self, locator):
        self.locator = locator
        self.stopped_moving = element_stops_moving(locator)

    def __call__(self, driver):
        elem = driver.find_element(*self.locator)
        stopped = self.stopped_moving(driver)

        if stopped != False and elem.is_displayed():
            return elem
        return False
