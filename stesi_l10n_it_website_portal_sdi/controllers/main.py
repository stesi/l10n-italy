from odoo import _
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale

CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(["codice_destinatario"])


class WebsiteSalePEC(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(WebsiteSalePEC, self)._checkout_form_save(
            mode, checkout, all_values)
        partner_values = dict()
        if 'codice_destinatario' not in checkout and 'codice_destinatario' in all_values:
            partner_values['codice_destinatario'] = all_values['codice_destinatario']
        if partner_values:
            request.env['res.partner'].browse(res).sudo().write(partner_values)
        return res
