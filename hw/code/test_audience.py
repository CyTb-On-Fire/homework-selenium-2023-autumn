from base import BaseCase
from ui.fixtures import audience_page, credentials
from ui.pages.audience_page import keywords_payload
import pytest


class TestAudience(BaseCase):
    keywords_name = 'Аудитория с ключевыми словами'

    def test_long_audience_name(self, audience_page):
        audience_page.set_audience_name('a'*256)
        audience_page.has_long_name_error()

    def test_create_keywords(self, audience_page):
        data = keywords_payload()
        audience_page.set_audience_name(self.keywords_name)
        audience_page.add_source(audience_page.KEYWORDS, data)
        assert audience_page.get_source(0) == data

    @pytest.mark.parametrize('days', ['31'])
    def test_create_keywords_invalid_days(self, audience_page, days):
        data = keywords_payload(days=days)
        audience_page.set_audience_name(self.keywords_name)
        audience_page.add_source(audience_page.KEYWORDS, data)
        assert audience_page.get_source(0)['days'] == '30'

    def test_edit_audience(self, audience_page):
        name = self.keywords_name
        audience_page.create_audience(name, data=keywords_payload())
        audience_page.open_edit_modal(name)
        audience_page.save_audience()
        audience_page.delete_audience(name)

    def test_boolean_rule(self, audience_page):
        audience_page.set_audience_name(self.keywords_name)

        audience_page.add_source(data=keywords_payload(name='Условие 1'))
        audience_page.add_source(data=keywords_payload(name='Условие 2'))

        audience_page.set_rule('и')
        assert audience_page.get_rule() == 'и'

        audience_page.set_rule('или')
        assert audience_page.get_rule() == 'или'
