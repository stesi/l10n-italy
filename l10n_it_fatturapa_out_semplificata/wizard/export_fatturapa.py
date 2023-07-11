from odoo import models, fields, api, _
from .efattura import EFatturaOut


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    # def exportFatturaPA(self):
    #     action = super(WizardExportFatturapa, self).exportFatturaPA()
    #     return action
    @api.model
    def _get_efattura_class(self):
        res = super(WizardExportFatturapa, self)._get_efattura_class()
        return EFatturaOut
