# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models

from .efattura import EFatturaOut

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export
from odoo.tools import float_repr


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def _get_efattura_class(self):
        efattura_class = super()._get_efattura_class()

        class EFatturaOut(efattura_class):

            def __init__(self, wizard, partner_id, invoices, progressivo_invio):
                res = super(EFatturaOut, self).__init__(wizard, partner_id, invoices, progressivo_invio)
                invoice = invoices[0]
                if invoice.move_type in [
                    "out_invoice", "out_refund"
                ] and invoice.fiscal_document_type_id.code in ["TD16", "TD17", "TD18", "TD19"]:
                    related_invoice = invoice.env['account.move'].search([('rc_self_invoice_id.id', '=', invoice.id)])
                    if len(related_invoice) > 0 and related_invoice[0].fiscal_position_id.rc_type_id.partner_id:
                        partner = related_invoice[0].fiscal_position_id.rc_type_id.partner_id
                        self.partner_id = partner
                return res

            def get_template_values(self):
                template_values = super().get_template_values()

                def format_numbers(number):
                    # format number to str with between 2 and 8 decimals (event if it's .00)
                    number_splited = str(number).split(".")
                    if len(number_splited) == 1:
                        return "%.02f" % number

                    cents = number_splited[1]
                    if len(cents) > 8:
                        return "%.08f" % number
                    return float_repr(number, max(2, len(cents)))

                def get_all_taxes(record):
                    """Generate summary data for taxes.
                    Odoo does that for us, but only for nonzero taxes.
                    SdI expects a summary for every tax mentioned in the invoice,
                    even those with price_total == 0.
                    """

                    def _key(tax_id):
                        return tax_id.id

                    out_computed = {}
                    # existing tax lines
                    tax_ids = record.line_ids.filtered(lambda line: line.tax_line_id)
                    for tax_id in tax_ids:
                        tax_line_id = tax_id.tax_line_id
                        aliquota = format_numbers(tax_line_id.amount)
                        aliquota_float = tax_line_id.amount
                        key = _key(tax_line_id)
                        imponibile_importo = 0  # fix problem with valuta estera
                        imponibile_importo = tax_id.tax_base_amount
                        if (tax_id.tax_base_amount * aliquota_float / 100) == tax_id.price_total:
                            imposta = tax_id.price_total
                        else:
                            # imponibile_importo = (tax_id.price_total * 100 / aliquota_float)
                            imposta = (tax_id.tax_base_amount * aliquota_float / 100)
                        out_computed[key] = {
                            "AliquotaIVA": aliquota,
                            "Natura": tax_line_id.kind_id.code,
                            # 'Arrotondamento':'',
                            # "ImponibileImporto": tax_id.tax_base_amount,
                            "ImponibileImporto": imponibile_importo,
                            # "Imposta": tax_id.price_total,
                            "Imposta": imposta,
                            "EsigibilitaIVA": tax_line_id.payability,
                        }
                        if tax_line_id.law_reference:
                            out_computed[key]["RiferimentoNormativo"] = encode_for_export(
                                tax_line_id.law_reference, 100
                            )

                    out = {}
                    # check for missing tax lines
                    for line in record.invoice_line_ids:
                        if line.display_type in ("line_section", "line_note"):
                            # notes and sections
                            # we ignore line.tax_ids altogether,
                            # (it is popolated with a default tax usually)
                            # and use another tax in the template
                            continue
                        for tax_id in line.tax_ids:
                            aliquota = format_numbers(tax_id.amount)
                            key = _key(tax_id)
                            if key in out_computed:
                                continue
                            if key not in out:
                                out[key] = {
                                    "AliquotaIVA": aliquota,
                                    "Natura": tax_id.kind_id.code,
                                    # 'Arrotondamento':'',
                                    "ImponibileImporto": line.price_subtotal,
                                    "Imposta": 0.0,
                                    "EsigibilitaIVA": tax_id.payability,
                                }
                                if tax_id.law_reference:
                                    out[key]["RiferimentoNormativo"] = encode_for_export(
                                        tax_id.law_reference, 100
                                    )
                            else:
                                out[key]["ImponibileImporto"] += line.price_subtotal
                                out[key]["Imposta"] += 0.0
                    out.update(out_computed)
                    return out

                if 'all_taxes' in template_values:
                    template_values['all_taxes'] = {invoice.id: get_all_taxes(invoice) for invoice in self.invoices}
                return template_values

        return EFatturaOut
