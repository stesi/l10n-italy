from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockDeliveryNote(models.Model):
    _inherit = 'stock.delivery.note'

    def multiple_action_invoice(self):
        for ddt in self:
            ddt.action_invoice()
