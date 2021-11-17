from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = "pos.order"


    def _prepare_invoice_vals(self):
        vals=super(PosOrder, self)._prepare_invoice_vals()
        if vals['journal_id']:
            public_user = self.env.ref('base.public_user').partner_id.id
            if self.partner_id.id == public_user:
                vals['journal_id'] = self.env['account.move'].with_context(default_corrispettivi=True)._get_default_journal().id
        return vals


    def schedule_as_corrispettivi(self):
        elements = self.env['pos.order'].search([('partner_id', '=', False), ('state', 'in', ['paid'])])
        for elem in elements:
            elem.partner_id = self.env.ref('base.public_partner').id
        return elements.action_pos_order_invoice()
