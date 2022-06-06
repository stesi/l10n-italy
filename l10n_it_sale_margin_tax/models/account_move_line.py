import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    margin_from_sale = fields.Float(compute='_compute_margin_from_sale',store=True)

    @api.depends('sale_line_ids','sale_line_ids.margin')
    def _compute_margin_from_sale(self):
        for aml in self:
            aml.margin_from_sale = sum(aml.sale_line_ids.margin)
    def update_margin(self):
        for aml in self:
            if aml.margin_from_sale:
                aml.margin =aml.margin_from_sale
