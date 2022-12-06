# Copyright 2014 Davide Corio
# Copyright 2016-2018 Lorenzo Battistini - Agile Business Group

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    force_export_vat = fields.Boolean(related="country_id.force_export_vat")
