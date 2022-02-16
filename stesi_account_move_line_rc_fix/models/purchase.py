from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_create_invoice(self):
        res = super(PurchaseOrder, self).action_create_invoice()
        if self.invoice_ids:
            for move in self.invoice_ids:
                for line in move.line_ids:
                    line._set_rc_flag(move)
        return res
