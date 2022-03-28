from odoo import models, api


class Order(models.Model):
    _inherit = "pos.order"

    def _send_e_invoice(self):
        self.account_move.fatturapa_attachment_out_id.send_via_pec()

    @api.model
    def create_from_ui(self, orders, draft=False):
        order_ids = super(Order, self).create_from_ui(orders,draft)
        for order in self.browse([order.get('id') for order in order_ids]):
            if (
                order.account_move and
                order.account_move.state in ("posted")
            ):
                wizard = self.env["wizard.export.fatturapa"].with_context(
                    active_id=order.account_move.id, active_ids=order.account_move.ids,
                    active_model="account.move"
                ).create({})
                wizard.exportFatturaPA()
                order._send_e_invoice()
        return order_ids
