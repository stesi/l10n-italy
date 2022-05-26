import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api

class AccountTax(models.Model):
    _inherit = 'account.tax'
    margin_tax = fields.Boolean()
