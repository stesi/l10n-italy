from odoo import api, fields, models, registry
from odoo.exceptions import UserError
from odoo.fields import first
from odoo.tools import float_is_zero
from odoo.tools.translate import _

class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"
    def get_line_product(self, line, partner):
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        fatturapa_in_search_by_default_code = IrConfigParameter.get_param("l10n_it_fatturapa_in.search_default_code", False)
        product = self.env["product.product"].browse()
        if fatturapa_in_search_by_default_code== 'True':
            if len(line.CodiceArticolo or []) == 1:
                code = line.CodiceArticolo[0].CodiceValore
                product = self.env['product.product'].search([('default_code','=',code)],limit=1)
        if fatturapa_in_search_by_default_code!= 'True' or len(product)==0:
            product= super(WizardImportFatturapa, self).get_line_product(line,partner)
        return product



