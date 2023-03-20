from odoo import _, api, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    partner_as_transferor = fields.Boolean()
