
from odoo import models, fields, api

class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'
    margin_tax_lot = fields.Boolean()
    purchase_price = fields.Float()

