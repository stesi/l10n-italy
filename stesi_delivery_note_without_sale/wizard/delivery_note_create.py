# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

import datetime

from odoo import api, fields, models


class StockDeliveryNoteCreateWizard(models.TransientModel):
    _inherit = "stock.delivery.note.create.wizard"

    def confirm(self):
        sale_order_ids = self.mapped("selected_picking_ids.sale_id")
        sale_order_id = sale_order_ids and sale_order_ids[0] or False
        if sale_order_id:
            super(StockDeliveryNoteCreateWizard, self).confirm()
        else:

            self.check_compliance(self.selected_picking_ids)

            delivery_note = self.env["stock.delivery.note"].create(
                {
                    "partner_sender_id": self.partner_sender_id.id,
                    "partner_id": self.partner_id.id,
                    "partner_shipping_id": self.partner_shipping_id.id,
                    "type_id": self.type_id.id,
                    "date": self.date,
                    "delivery_method_id": self.partner_id.property_delivery_carrier_id.id,
                    "transport_condition_id": sale_order_id
                    and sale_order_id.default_transport_condition_id.id
                    or self.partner_id.default_transport_condition_id.id
                    or self.type_id.default_transport_condition_id.id,
                    "goods_appearance_id": sale_order_id
                    and sale_order_id.default_goods_appearance_id.id
                    or self.partner_id.default_goods_appearance_id.id
                    or self.type_id.default_goods_appearance_id.id,
                    "transport_reason_id": sale_order_id
                    and sale_order_id.default_transport_reason_id.id
                    or self.partner_id.default_transport_reason_id.id
                    or self.type_id.default_transport_reason_id.id,
                    "transport_method_id": sale_order_id
                    and sale_order_id.default_transport_method_id.id
                    or self.partner_id.default_transport_method_id.id
                    or self.type_id.default_transport_method_id.id,
                }
            )

            self.selected_picking_ids.write({"delivery_note_id": delivery_note.id})

            if self.user_has_groups("l10n_it_delivery_note.use_advanced_delivery_notes"):
                return delivery_note.goto()
