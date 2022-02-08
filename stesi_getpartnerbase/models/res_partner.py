import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api


class Respartner(models.Model):
    _inherit = 'res.partner'
    partner_def_e_fattura = fields.Boolean()
    @api.constrains('partner_def_e_fattura')
    def check_def_e_fattura(self):
        if self.partner_def_e_fattura:
            check_partner = self.env['res.partner'].search([('vat','=',self.vat),('partner_def_e_fattura','=',True)],limit=1)
            if len(check_partner)==0:
                check_partner = self.env['res.partner'].search(
                    [('fiscalcode', '=', self.fiscalcode), ('partner_def_e_fattura', '=', True)], limit=1)
            if len(check_partner):
                self.partner_def_e_fattura = False
