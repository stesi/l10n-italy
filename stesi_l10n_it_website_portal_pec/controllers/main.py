from odoo import _
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale

CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(["pec_mail"])


class WebsiteSalePEC(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(WebsiteSalePEC, self)._checkout_form_save(
            mode, checkout, all_values)
        partner_values = dict()
        if 'pec_mail' not in checkout and 'pec_mail' in all_values:
            partner_values['pec_mail'] = all_values['pec_mail']
        if partner_values:
            request.env['res.partner'].browse(res).sudo().write(partner_values)
        return res
