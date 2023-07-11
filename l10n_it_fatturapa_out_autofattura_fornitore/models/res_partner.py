
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    fatturapa_out_autofattura = fields.Boolean()


