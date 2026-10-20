{
    'name': 'OSZ - Menú de aplicaciones',
    'summary': 'Aplicaciones en cuadrícula, búsqueda y tema claro u oscuro',
    'version': '19.0.1.0.0',
    'author': 'OSZ',
    'license': 'LGPL-3',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'osz_app_launcher/static/src/launcher.js',
            'osz_app_launcher/static/src/launcher.xml',
            'osz_app_launcher/static/src/launcher.scss',
        ],
    },
    'installable': True,
}
