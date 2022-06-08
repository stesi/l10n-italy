import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    margin = fields.Float()
    is_margin_tax_line = fields.Boolean()
    @api.onchange('margin')
    def _on_change_margin(self):
        for line in self:
            if not line.tax_repartition_line_id:
                line.recompute_tax_line = True
