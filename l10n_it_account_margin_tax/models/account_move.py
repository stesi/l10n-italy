import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'
    is_margin_tax_invoice=fields.Boolean(compute='_compute_is_margin_tax_invoice')
    def _compute_is_margin_tax_invoice(self):
        for am in self:
            am.is_margin_tax_invoice = len(am.line_ids.filtered(lambda l: l.tax_ids.filtered(lambda t: t.margin_tax))) >0

    # def button_draft(self):
    #     for am in self:
    #         super(AccountMove, am).button_draft()
    #         am.generate_margin_tax_lines()

    def _recompute_tax_lines(self,recompute_tax_base_amount=False):
        for am in self:
            if am.is_margin_tax_invoice and not am.company_id.mt_account_id:
                raise ValidationError(
                    _("Margin tax account not set")
                )
            margin_tax_lines = am.line_ids.filtered(lambda l:l.tax_ids.filtered(lambda t: t.margin_tax))
            margin_tax_lines_dynamic = am.line_ids.filtered(lambda l:l.is_margin_tax_line)

            if len(margin_tax_lines_dynamic)>0:
                am.line_ids -=margin_tax_lines_dynamic#.with_context(check_move_validity=False).unlink()
                # am.refresh()
                # am.with_context(check_move_validity=False)._recompute_dynamic_lines()
            super(AccountMove, am)._recompute_tax_lines(recompute_tax_base_amount=recompute_tax_base_amount)
            if len(margin_tax_lines)>0:
                tax_id = margin_tax_lines.mapped('tax_ids').filtered(lambda t: t.margin_tax)
                base_amount = sum(
                    margin_tax_lines.filtered(lambda t: t.margin > 0).mapped('margin'))
                tax_amount = base_amount* tax_id.orig_percentage / 100
                invoice_repartition_line_id = tax_id.invoice_repartition_line_ids.filtered(
                    lambda l: l.factor_percent == 100 and l.repartition_type == 'tax')
                if len(invoice_repartition_line_id) == 0:
                    raise UserError(_("No repartition set on tax"))
                account_id_default = invoice_repartition_line_id[0].account_id
                invoice_repartition_line_id =  invoice_repartition_line_id.id.origin if isinstance(invoice_repartition_line_id.id,models.NewId) else invoice_repartition_line_id.id
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

                    # 'move_id':am.id
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
                    "tax_base_amount": base_amount,
                    "tax_repartition_line_id": invoice_repartition_line_id,
                    # 'move_id': am.id
                }

                vals = []
                vals.append(vals_credit)
                vals.append(vals_debit)
                #
                #30
                move_line1= self.env['account.move.line'].new(vals_debit)
                move_line2= self.env['account.move.line'].new(vals_credit)
                am.line_ids +=move_line1 + move_line2

    @api.depends('line_ids.price_subtotal', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id', 'currency_id')
    def _compute_invoice_taxes_by_group(self):
        super(AccountMove, self)._compute_invoice_taxes_by_group()
        margin_tax_lines = self.line_ids.filtered(lambda l: l.tax_line_id.filtered(lambda t: t.margin_tax) )
        if len(margin_tax_lines)>0:
            self.amount_by_group = []

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()
        margin_tax_lines = self.line_ids.filtered(lambda l: l.tax_line_id.filtered(lambda t: t.margin_tax) )
        if len(margin_tax_lines)>0:
            self.amount_total = self.amount_untaxed
            self.amount_tax =0
    def action_post(self):
        for am in self:
            if am.is_margin_tax_invoice:
                margin_tax_lines = am.invoice_line_ids.filtered(lambda l: l.tax_ids.filtered(lambda t: t.margin_tax))
                if len(margin_tax_lines) != len(am.invoice_line_ids.filtered(lambda l:not l.display_type)):
                    raise   ValidationError(_("The invoice contains margin tax lines and non margin tax lines"))
        return super(AccountMove, self).action_post()






