# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_round

class AccountMove(models.Model):
    _inherit = "account.move"

    def button_draft(self):
        for move in self:
            account_wt = self.env['account.move']
            if move.move_type == "in_invoice":
                account_wt = move.line_ids.filtered(lambda line: line.account_id.user_type_id.type in (
                    'receivable', 'payable')).matched_debit_ids.debit_move_id.filtered(
                    lambda l1: l1.filtered(lambda l1: l1.withholding_tax_generated_by_move_id.id > 0)).move_id
            elif move.move_type == "out_invoice":
                account_wt = move.line_ids.filtered(lambda line: line.account_id.user_type_id.type in (
                    'receivable', 'payable')).matched_credit_ids.credit_move_id.filtered(
                    lambda l1: l1.filtered(lambda l1: l1.withholding_tax_generated_by_move_id.id > 0)).move_id
            if len(account_wt) > 0:
                account_wt.posted_before = False
                #account_wt.button_draft()
                account_wt.button_cancel()

                # reconcile = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type in (
                # 'receivable', 'payable')).matched_credit_ids.credit_move_id.filtered(
                # lambda l1: l1.filtered(lambda l1: l1.withholding_tax_generated_by_move_id.id > 0))
                # if len(reconcile):
                #     reconcile.unlink()
                # account_wt.unlink()
                if move.move_type == "in_invoice":
                    wt_moves = move.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')) \
                        .mapped('matched_debit_ids.wt_tax_moves')
                elif move.move_type == "out_invoice":
                    wt_moves = move.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')) \
                        .mapped('matched_credit_ids.wt_tax_moves')

                for wt in wt_moves:
                    wt.unlink()
                domain = [("move_id", "=", move.id)]
                wt_statements = self.env["withholding.tax.statement"].search(domain)
                for wt in wt_statements:
                    wt.unlink()
            # wt_lines = self.withholding_tax_line_ids
            # for wt in wt_lines:
            #     wt.unlink()


        return super(AccountMove, self).button_draft()


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    wt_tax_moves = fields.One2many('withholding.tax.move','reconcile_partial_id', "Wt tax moves")
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
