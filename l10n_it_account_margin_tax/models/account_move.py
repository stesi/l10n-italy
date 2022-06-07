import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api,_
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'


    def generate_margin_tax_lines(self):
        for am in self:
            margin_tax_lines = am.line_ids.filtered(lambda l:l.tax_ids.filtered(lambda t: t.margin_tax))
            margin_tax_lines_dynamic = am.line_ids.filtered(lambda l:l.is_margin_tax_line)

            if len(margin_tax_lines_dynamic)>0:
                margin_tax_lines_dynamic.unlink()
            if len(margin_tax_lines)>0:
                tax_id = margin_tax_lines.mapped('tax_ids').filtered(lambda t: t.margin_tax)
                tax_amount = sum(
                    margin_tax_lines.filtered(lambda t: t.margin > 0).mapped('margin')) * tax_id.orig_percentage / 100
                account_id_default = tax_id.invoice_repartition_line_ids.filtered(
                    lambda l: l.factor_percent == 100 and l.repartition_type == 'tax')
                if len(account_id_default) == 0:
                    raise UserError(_("No account set on tax"))
                account_id_default = account_id_default[0].account_id
                vals_debit = {
                    "name": _("Margin Tax Debit"),
                    "partner_id": self.partner_id.id,
                    "account_id": self.company_id.mt_account_id.id,
                    "journal_id": self.journal_id.id,
                    "date": self.invoice_date,
                    "debit": tax_amount,
                    "credit": 0,
                    "exclude_from_invoice_tab": True,
                    "is_margin_tax_line": True,
                    'move_id':am.id
                }
                vals_credit = {
                    "name": _("Margin Tax Credit"),
                    "partner_id": self.partner_id.id,
                    "account_id": account_id_default.id,
                    "journal_id": self.journal_id.id,
                    "date": self.invoice_date,
                    "debit": 0,
                    "credit": tax_amount,
                    "exclude_from_invoice_tab": True,
                    "is_margin_tax_line": True,
                    'move_id': am.id
                }
                vals = []
                vals.append(vals_credit)
                vals.append(vals_debit)


                self.env['account.move.line'].create(vals)






