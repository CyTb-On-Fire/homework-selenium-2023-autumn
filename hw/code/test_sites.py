from base import BaseCase
from ui.fixtures import sites_page
import pytest


class TestSites(BaseCase):
    def test_add_pixel_modal(self, sites_page):
        sites_page.open_add_pixel_modal()
        sites_page.check_pixel_modal_opened()

        sites_page.close_add_pixel_modal()
        sites_page.check_pixel_modal_closed()

    def test_add_pixel_modal_submit_btn(self, sites_page):
        sites_page.open_add_pixel_modal()

        assert not sites_page.submit_btn_enabled()

        sites_page.fill_domain_input("wild-spirits.test")

        assert sites_page.submit_btn_enabled()

        sites_page.click_submit_btn()

        sites_page.check_pixel_created_modal()
