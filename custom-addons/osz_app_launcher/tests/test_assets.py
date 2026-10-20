from lxml import html

from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestLauncherAssets(HttpCase):
    def test_backend_styles_compile_with_launcher(self):
        self.authenticate('admin', 'admin')
        response = self.url_open('/odoo')
        self.assertEqual(response.status_code, 200)
        page = html.fromstring(response.content)
        stylesheets = page.xpath('//link[@rel="stylesheet" and contains(@href, "/web/assets/")]/@href')
        self.assertTrue(stylesheets, 'Backend must load compiled stylesheets')
        css = ''
        for url in stylesheets:
            asset = self.url_open(url)
            self.assertEqual(asset.status_code, 200)
            css += asset.text
        self.assertNotIn('A css error', css)
        self.assertIn('.osz-launcher-dialog', css)
        self.assertIn('.osz-app-grid', css)
