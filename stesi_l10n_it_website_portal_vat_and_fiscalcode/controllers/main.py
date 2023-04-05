from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale, WebsiteSaleForm

CustomerPortal.OPTIONAL_BILLING_FIELDS.extend(["fiscalcode", "vat"])

class WebsiteSaleFormFiscalCode(WebsiteSaleForm):
    @http.route('/website_form/shop.sale.order', type='http', auth="public", methods=['POST'], website=True)
    def website_form_saleorder(self, **kwargs):
        res = super(WebsiteSaleFormFiscalCode, self).website_form_saleorder(**kwargs)
        order = request.website.sale_get_order()
        partner = order.partner_id
        if partner and kwargs.get("fiscalcode"):
            partner.update({
                'fiscalcode': str(kwargs.get("fiscalcode"))
            })
        return res

class WebsiteSaleFiscalCode(WebsiteSale):


    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data)
        partner_sudo = request.env.user.partner_id.sudo()
        dummy_partner = request.env['res.partner'].new({
            'fiscalcode': data.get('fiscalcode'),
            'is_company': partner_sudo.is_company
        })
        if not dummy_partner.check_fiscalcode():
            error['fiscalcode'] = 'error'
            error_message.append(_('Fiscal Code not valid'))
        if not data.get('vat') and partner_sudo.company_type == 'company':
            error['vat'] = 'error'
            error_message.append(_('Vat is required'))
        return error, error_message


class WebsitePortalFiscalCode(CustomerPortal):

    def details_form_validate(self, data):
        error, error_message = super(
            WebsitePortalFiscalCode, self
        ).details_form_validate(data)
        # Check fiscalcode
        partner = request.env.user.partner_id
        # company_type does not come from page form
        company_type = partner.company_type
        company_name = False
        if "company_name" in data:
            company_name = data.get("company_name")
        else:
            # when company_name is not posted (readonly)
            if partner.company_name:
                company_name = partner.company_name
            elif partner.company_type == "company":
                company_name = partner.name
        dummy_partner = request.env["res.partner"].new(
            {
                "fiscalcode": data.get("fiscalcode"),
                "vat": data.get("vat"),
                "company_name": company_name,
                "company_type": company_type,
            }
        )
        try:
            dummy_partner.check_fiscalcode()
        except ValidationError as e:
            error["fiscalcode"] = "error"
            error["vat"] = "error"
            error_message.append(e)
        return error, error_message
