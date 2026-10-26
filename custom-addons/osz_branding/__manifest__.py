{
    'name': 'OSZ ERP - Identidad',
    'version': '19.0.3.0.0',
    'author': 'OSZ',
    'license': 'LGPL-3',
    'depends': ['muk_web_theme'],
    'data': ['data/language.xml', 'views/layout.xml'],
    'assets': {'web.assets_backend': [
        'osz_branding/static/src/js/branding.js',
        'osz_branding/static/src/xml/branding.xml',
    ]},
    'installable': True,
}
