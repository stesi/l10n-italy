from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    simplified_einvoice = fields.Boolean(string="Simplified E-Invoice", index=True)
