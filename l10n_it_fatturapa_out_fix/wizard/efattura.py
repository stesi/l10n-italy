from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (
    EFatturaOut as _EFatturaOut,
)

class EFatturaOut(_EFatturaOut):

    def get_template_values(self):
        template_values = super().get_template_values()
        force_vat = False
        if template_values['partner_id']:
            force_vat =  template_values['partner_id'].country_id.force_export_vat
        template_values['force_vat'] = force_vat
        return template_values
