import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    margin = fields.Float()

