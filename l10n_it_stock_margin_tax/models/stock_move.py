
from odoo import models, fields, api

class stock_move(models.Model):
    _inherit = 'stock.move'
    margin_tax = fields.Boolean()
    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        merge_values = super(stock_move, self)._prepare_merge_moves_distinct_fields()
        merge_values.append('margin_tax')
        return merge_values
