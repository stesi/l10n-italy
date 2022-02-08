import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError

class Respartner(models.Model):
    _inherit = 'res.partner'
    partner_def_e_fattura = fields.Boolean()
    def check_if_partner_exist(self):
        check_partner_count=0
        if self.vat:
            domain = [('vat', '=', self.vat), ('partner_def_e_fattura', '=', True)]
            if isinstance(self.id,int):
                domain.append(('id','=',self.id))
            check_partner = self.env['res.partner'].search(domain,
                                                           limit=1)
            check_partner_count = len(check_partner)
        if check_partner_count == 0 and self.fiscalcode:
            domain =[('fiscalcode', '=', self.fiscalcode), ('partner_def_e_fattura', '=', True)]
            if isinstance(self.id,int):
                domain.append(('id','=',self.id))
            check_partner = self.env['res.partner'].search(domain
                , limit=1)
            check_partner_count = len(check_partner)
        if check_partner_count>0:
            exist = True
        else:
            exist=False
        return exist
    @api.constrains('partner_def_e_fattura')
    def check_def_e_fattura(self):

            if self.check_if_partner_exist():
                self.partner_def_e_fattura = False
    @api.onchange('partner_def_e_fattura')
    def check_def_e_fattura(self):

            if self.check_if_partner_exist():
                #raise ValidationError(_('Already exist a default partner with same VAT or Fiscal code'))
                self.partner_def_e_fattura = False
                return {

                    'warning': {

                        'title': 'Warning!',

                        'message': _('Already exist a default partner with same VAT or Fiscal code.')}

                }
