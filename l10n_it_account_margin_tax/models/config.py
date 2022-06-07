# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    mt_account_id = fields.Many2one(
        "account.account",
        string="Margin tax account",
        help="Account used to write off the VAT amount",
        readonly=False,
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mt_account_id = fields.Many2one(
        related="company_id.mt_account_id",
        string="Margin tax account",
        help="Account used to write off the VAT amount",
        readonly=False,
    )
