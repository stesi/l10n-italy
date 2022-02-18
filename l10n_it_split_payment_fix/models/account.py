# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_split_payments(self):
        write_off_line_vals = self._build_debit_line()
        line_sp = self.line_ids.filtered(lambda l: l.is_split_payment)
        if line_sp:
            if self.move_type == "out_invoice" and float_compare(
                line_sp[0].debit,
                write_off_line_vals["debit"],
                precision_rounding=self.currency_id.rounding,
            ):
                line_sp[0].with_context(check_move_validity=False).update({"debit": 0})
                self.set_receivable_line_ids()
                line_sp[0].debit = write_off_line_vals["debit"]
            elif self.move_type == "out_refund" and float_compare(
                line_sp[0].credit,
                write_off_line_vals["credit"],
                precision_rounding=self.currency_id.rounding,
            ):
                line_sp[0].with_context(check_move_validity=False).update({"credit": 0})
                self.set_receivable_line_ids()
                line_sp[0].credit = write_off_line_vals["credit"]
        else:

            if self.amount_sp:
                self.line_ids = [(0, 0, write_off_line_vals)]
            self.set_receivable_line_ids()
