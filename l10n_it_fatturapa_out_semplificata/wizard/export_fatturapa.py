from odoo import models, fields, api, _


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    # def exportFatturaPA(self):
    #     action = super(WizardExportFatturapa, self).exportFatturaPA()
    #     return action

