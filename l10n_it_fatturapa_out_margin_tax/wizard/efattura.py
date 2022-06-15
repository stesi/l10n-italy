# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (
    EFatturaOut as _EFatturaOut,
)


# extend the EFatturaOut class to add a new helper function
class EFatturaOut(_EFatturaOut):
    def get_template_values(self):


        res = super().get_template_values()
        invoices_taxes = res['all_taxes']
        for invoice in invoices_taxes:
            for tax in invoices_taxes[invoice]:
                tax_id = self.env['account.tax'].browse(tax)
                if tax_id.margin_tax:
                    invoices_taxes[invoice][tax]['Imposta'] = 0
                    invoices_taxes[invoice][tax]['ImponibileImporto'] = self.env['account.move'].browse(invoice).amount_total
        return res
