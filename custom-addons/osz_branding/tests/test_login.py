from lxml import html

from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestBrandedLogin(HttpCase):
    def test_login_keeps_form_and_brand(self):
        response = self.url_open('/web/login', headers={'Accept-Language': 'en-US,en;q=0.9'})
        self.assertEqual(response.status_code, 200)
        page = html.fromstring(response.content)
        self.assertEqual(page.xpath('string(//title)').strip(), 'OSZ ERP')
        self.assertTrue(page.xpath('//form//input[@name="login"]'))
        self.assertTrue(page.xpath('//form//input[@name="password"]'))
        self.assertTrue(page.xpath('//img[@alt="OSZ ERP" and @src="/osz_branding/static/img/osz-erp.svg"]'))
        self.assertTrue(page.xpath('//a[contains(@href, "odoo.com")]'), 'Keep the Odoo attribution')
        self.assertTrue(page.xpath('//link[@rel="shortcut icon" and @href="/osz_branding/static/img/favicon.svg"]'))
        self.assertIn('Iniciar sesión', page.text_content())
        self.assertIn('Contraseña', page.text_content())
        self.assertNotIn('Log in', page.text_content())
        self.assertTrue(page.xpath('//div[@id="osz_customization_credit"]/a[@href="https://onesecurezone.com/"]'))
        self.assertIn('Personalizado por', page.text_content())

    def test_liquid_glass_backend_assets(self):
        self.authenticate('admin', 'admin')
        page = html.fromstring(self.url_open('/odoo').content)
        urls = page.xpath('//link[@rel="stylesheet" and contains(@href, "/web/assets/")]/@href')
        self.assertTrue(urls)
        css = ''
        for url in urls:
            response = self.url_open(url)
            self.assertEqual(response.status_code, 200)
            css += response.text
        self.assertNotIn('A css error', css)
        self.assertIn('.o_apps_sidebar', css)
        self.assertNotIn('.osz-launcher-dialog', css)
        self.assertEqual(self.env['ir.module.module'].search([('name', '=', 'theme_liquid_glass')]).state, 'installed')
