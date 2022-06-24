import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError
class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    def _set_manual_margin_from_lot(self):
        for pol in self:
            if pol.pack_lot_ids:
                lot_id = self.env['stock.production.lot'].search([('product_id','=',pol.pack_lot_ids[0].product_id.id),('name','=',pol.pack_lot_ids[0].lot_name),('company_id','=',self.env.company.id)])
                pol.manual_purchase_price = lot_id.purchase_price
