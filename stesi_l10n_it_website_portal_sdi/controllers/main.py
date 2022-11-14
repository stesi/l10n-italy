from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale, WebsiteSaleForm

CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(["codice_destinatario"])


class WebsiteSaleFormSDI(WebsiteSaleForm):
    @http.route('/website_form/shop.sale.order', type='http', auth="public", methods=['POST'], website=True)
    def website_form_saleorder(self, **kwargs):
        res = super(WebsiteSaleFormSDI, self).website_form_saleorder(**kwargs)
        order = request.website.sale_get_order()
        partner = order.partner_id
        if partner and kwargs.get("codice_destinatario"):
            partner.update({
                'codice_destinatario': str(kwargs.get("codice_destinatario"))
            })
        return res
