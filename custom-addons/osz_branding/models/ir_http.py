from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls, endpoint):
        # Public authentication screens have no user preference yet. Apply the
        # product's language only here; never change a user's saved language.
        if request.httprequest.path.rstrip('/') in {
            '/web/login', '/web/signup', '/web/reset_password',
        }:
            lang = request.env['res.lang']._get_data(code='es_PE')
            if lang:
                request.update_context(lang=lang.code)
                # http_routing uses this for frontend session information.
                if hasattr(request, 'lang'):
                    request.lang = lang
        return super()._dispatch(endpoint)
