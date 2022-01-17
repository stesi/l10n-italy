# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import api, fields, models


class StockDeliveryNoteSelectWizard(models.TransientModel):
    _inherit = "stock.delivery.note.select.wizard"

    def confirm(self):
        sale_order_ids = self.mapped("selected_picking_ids.sale_id")
        sale_order_id = sale_order_ids and sale_order_ids[0] or False
        if sale_order_id:
            return super(StockDeliveryNoteSelectWizard, self).confirm()
        else:
            self.check_compliance(self.picking_ids)
            self.selected_picking_ids.write({"delivery_note_id": self.delivery_note_id.id})

            if self.user_has_groups("l10n_it_delivery_note.use_advanced_delivery_notes"):
                return self.delivery_note_id.goto()
