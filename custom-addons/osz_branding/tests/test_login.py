from lxml import html

from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestBrandedLogin(HttpCase):
    def test_login_keeps_form_and_brand(self):
        response = self.url_open('/web/login')
        self.assertEqual(response.status_code, 200)
        page = html.fromstring(response.content)
        self.assertEqual(page.xpath('string(//title)').strip(), 'OSZ ERP')
        self.assertTrue(page.xpath('//form//input[@name="login"]'))
        self.assertTrue(page.xpath('//form//input[@name="password"]'))
