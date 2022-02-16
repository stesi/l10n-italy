from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        res = super(SaleAdvancePaymentInv, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if sale_orders.invoice_ids:
            for move in sale_orders.invoice_ids:
                for line in move.line_ids:
                    line._set_rc_flag(move)
        return res
