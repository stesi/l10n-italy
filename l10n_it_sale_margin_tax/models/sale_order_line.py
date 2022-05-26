import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    margin_tax = fields.Boolean()
    def _compute_tax_id(self):
        for line in self:
            if line.margin_tax:
                line = line.with_company(line.company_id)
                fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(
                    line.order_partner_id.id)
                taxes = self.env['account.tax'].search([('margin_tax','=',True)],limit=1)
                if len(taxes)==0:
                    super(SaleOrderLine, line)._compute_tax_id()
                else:
                    line.tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id)
            else:
                super(SaleOrderLine, line)._compute_tax_id()
    @api.onchange('margin_tax')
    def margin_tax_onchange(self):
        for line in self:
            line.product_id_change()
