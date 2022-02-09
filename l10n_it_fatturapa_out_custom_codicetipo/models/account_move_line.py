# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api
import json
import urllib3
import ssl
import string
import random
import re

class account_move_line(models.Model):
    _inherit = 'account.move.line'
    value_type_for_efattura = fields.Char(compute='_compute_value_type_for_efattura')
    value_value_for_efattura = fields.Char(compute='_compute_value_type_for_efattura')

    def _compute_value_type_for_efattura(self):
        for aml in self:
            if aml.move_id.code_type and aml.move_id.code_value:
                aml.value_type_for_efattura = aml.move_id.code_type
                aml.value_value_for_efattura = aml.move_id.code_value
            else:
                if aml.product_id.barcode:
                    aml.value_type_for_efattura = 'EAN'
                    aml.value_value_for_efattura = aml.product_id.barcode[:35]
                elif aml.product_id.default_code:
                    aml.value_type_for_efattura = self.env['ir.config_parameter'].sudo().get_param('fatturapa.codicetipo.odoo', 'ODOO')
                    aml.value_value_for_efattura = aml.default_code.barcode[:35]
                else:
                    aml.value_type_for_efattura = self.env['ir.config_parameter'].sudo().get_param('fatturapa.codicetipo.odoo', 'ODOO')
                    aml.value_value_for_efattura = "000000"



