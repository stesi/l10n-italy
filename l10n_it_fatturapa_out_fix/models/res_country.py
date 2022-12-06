# Copyright 2014 Davide Corio
# Copyright 2016-2018 Lorenzo Battistini - Agile Business Group

from odoo import _, api, fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    force_export_vat = fields.Boolean(default=False)
