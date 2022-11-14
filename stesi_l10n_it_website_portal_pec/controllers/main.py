from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale, WebsiteSaleForm

CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(["pec_mail"])


class WebsiteSaleFormPEC(WebsiteSaleForm):
    @http.route('/website_form/shop.sale.order', type='http', auth="public", methods=['POST'], website=True)
    def website_form_saleorder(self, **kwargs):
        res = super(WebsiteSaleFormPEC, self).website_form_saleorder(**kwargs)
        order = request.website.sale_get_order()
        partner = order.partner_id
        if partner and kwargs.get("pec_mail"):
            partner.update({
                'pec_mail': str(kwargs.get("pec_mail"))
            })
        return res
