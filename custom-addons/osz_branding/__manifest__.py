{
    'name': 'OSZ ERP - Identidad',
    'version': '19.0.2.0.0',
    'author': 'OSZ',
    'license': 'LGPL-3',
    'depends': ['theme_liquid_glass'],
    'data': ['views/layout.xml'],
    'assets': {'web.assets_backend': [
        'osz_branding/static/src/js/branding.js',
        'osz_branding/static/src/xml/branding.xml',
    ]},
    'installable': True,
}
