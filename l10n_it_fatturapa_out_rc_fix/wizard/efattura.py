# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_fatturapa_out_rc.wizard.efattura import (
    EFatturaOut as _EFatturaOut,
)



# extend the EFatturaOut class to add a new helper function
class EFatturaOut(_EFatturaOut):

    def __init__(self, wizard, partner_id, invoices, progressivo_invio):
        res = super(EFatturaOut, self).__init__(wizard, partner_id, invoices, progressivo_invio)
        invoice = invoices[0]
        if invoice.move_type in [
            "out_invoice"
        ] and invoice.fiscal_document_type_id.code in ["TD16", "TD17", "TD18", "TD19"]:
            related_invoice = invoice.env['account.move'].search([('rc_self_invoice_id.id', '=', invoice.id)])
            if len(related_invoice) > 0 and related_invoice[0].fiscal_position_id.rc_type_id.partner_id:
                partner = related_invoice[0].fiscal_position_id.rc_type_id.partner_id
                self.partner_id = partner
        return res

    # def get_template_values(self):
    #     template_values = super().get_template_values()
    #     return template_values


