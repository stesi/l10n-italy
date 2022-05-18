# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_round

class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    @api.model
    def generate_wt_moves(self):
        wt_statement_obj = self.env["withholding.tax.statement"]
        # Reconcile lines
        line_payment_ids = []
        line_payment_ids.append(self.debit_move_id.id)
        line_payment_ids.append(self.credit_move_id.id)
        domain = [("id", "in", line_payment_ids)]
        rec_line_model = self.env["account.move.line"]
        rec_lines = rec_line_model.search(domain)

        # Search statements of competence
        wt_statements = wt_statement_obj.browse()
        rec_line_statement = rec_line_model.browse()
        for rec_line in rec_lines:
            domain = [("move_id", "=", rec_line.move_id.id)]
            wt_statements = wt_statement_obj.search(domain)
            if wt_statements:
                rec_line_statement = rec_line
                break
        # Search payment move
        rec_line_payment = rec_line_model.browse()
        for rec_line in rec_lines:
            if rec_line.id != rec_line_statement.id:
                rec_line_payment = rec_line
        # Generate wt moves
        wt_moves = []
        for wt_st in wt_statements:
            amount_wt = wt_st.get_wt_competence(self.amount)
            if amount_wt == 0:
                continue
            # Date maturity
            p_date_maturity = False
            payment_lines = wt_st.withholding_tax_id.payment_term.compute(
                amount_wt, rec_line_payment.date or False
            )
            if payment_lines and payment_lines[0]:
                p_date_maturity = payment_lines[0][0]
            wt_move_vals = {
                "statement_id": wt_st.id,
                "date": rec_line_payment.date,
                "partner_id": rec_line_statement.partner_id.id,
                "reconcile_partial_id": self.id,
                "payment_line_id": rec_line_payment.id,
                "credit_debit_line_id": rec_line_statement.id,
                "withholding_tax_id": wt_st.withholding_tax_id.id,
                "account_move_id": rec_line_payment.move_id.id or False,
                "date_maturity": p_date_maturity or rec_line_payment.date_maturity,
                "amount": amount_wt,
            }
            wt_move_vals = self._prepare_wt_move(wt_move_vals)
            wt_move = self.env["withholding.tax.move"].create(wt_move_vals)
            wt_moves.append(wt_move)
            # Generate account move
            wt_move.generate_account_move()
        return wt_moves
