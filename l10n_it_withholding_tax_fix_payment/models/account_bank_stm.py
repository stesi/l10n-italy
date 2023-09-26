from odoo import fields, models, api, _


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.model
    def _prepare_counterpart_move_line_vals(self, counterpart_vals, move_line=None):
        res = super(AccountBankStatementLine, self)._prepare_counterpart_move_line_vals(counterpart_vals, move_line)
        if move_line:
            debit = res.get("debit")
            credit = res.get("credit")
            if (debit or credit) and move_line.withholding_tax_amount:
                if credit < 0:
                    credit = move_line.amount_residual + move_line.withholding_tax_amount
                elif debit >= 0:
                    debit = abs(move_line.amount_residual) - move_line.withholding_tax_amount

                res.update({'credit': credit, 'debit': debit})

        return res
