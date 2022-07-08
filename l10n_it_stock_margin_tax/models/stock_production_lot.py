
from odoo import models, fields, api

class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'
    margin_tax_lot = fields.Boolean()
    purchase_price = fields.Float()
    location_id = fields.Many2one('stock.location',compute='_compute_location_id',search="_search_location_id")
    def _compute_location_id(self):
        for sp in self:
            sp.location_id = False
            quant_ids = sp.quant_ids.filtered(lambda l: l.location_id.usage =='internal' and l.quantity>0)
            if len(quant_ids)>0:
                quant_id = quant_ids[0]

                sp.location_id = quant_id.location_id
    def _search_location_id(self, operator, value):
        stock_quant = self.env['stock.quant'].search([('location_id',operator,value),('location_id.usage','=',"internal"),('quantity','>',0)])
        return [('id', 'in', stock_quant.mapped('lot_id').ids)]



