from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"


