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
                IrConfigParameter = self.env["ir.config_parameter"].sudo()
                auto_send_invoice = IrConfigParameter.get_param("auto_send_invoice","0")
                if auto_send_invoice =="1":
                    order._send_e_invoice()
        return order_ids
