
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class AccountInvoice(models.Model):
    _inherit = "account.move"

    def preventive_checks(self):
        for invoice in self:
            if invoice.partner_id.fatturapa_out_autofattura:


                if (
                    invoice.invoice_payment_term_id
                    and invoice.invoice_payment_term_id.fatturapa_pt_id.code is False
                ):
                    raise UserError(
                        _(
                            "Invoice %s fiscal payment term must be"
                            " set for the selected payment term %s",
                            invoice.name,
                            invoice.invoice_payment_term_id.name,
                        )
                    )

                if (
                    invoice.invoice_payment_term_id
                    and invoice.invoice_payment_term_id.fatturapa_pm_id.code is False
                ):
                    raise UserError(
                        _(
                            "Invoice %s fiscal payment method must be"
                            " set for the selected payment term %s",
                            invoice.name,
                            invoice.invoice_payment_term_id.name,
                        )
                    )

                if not all(
                    aml.tax_ids for aml in invoice.invoice_line_ids if aml.product_id
                ):
                    raise UserError(
                        _("Invoice %s contains product lines w/o taxes") % invoice.name
                    )
                company_id = invoice.company_id
                if company_id.vat != company_id.partner_id.vat:
                    raise UserError(
                        _("Invoice %s: company and company partner must have same vat")
                        % invoice.name
                    )
            else:
                super().preventive_checks()

