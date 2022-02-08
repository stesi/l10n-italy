import logging


from odoo import api, fields, models, registry



_logger = logging.getLogger(__name__)



class AccountMove(models.Model):
    _inherit = "account.move"
    code_type = fields.Char()
    code_value = fields.Char()
