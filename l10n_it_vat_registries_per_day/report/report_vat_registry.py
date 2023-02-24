
from odoo import api, models


class ReportVatRegistry(models.AbstractModel):
    _inherit= "report.l10n_it_vat_registries.report_registro_iva"

    @api.model
    def _get_report_values(self, docids, data=None):
        res = super()._get_report_values(docids,data)
        res["line_per_day"] = self._get_lines_per_day
        if self.env.context.get("active_id",False):
            wizard_id = self.env["wizard.registro.iva"].browse(self.env.context.get("active_id",False))
            res["only_totals_per_day"] = wizard_id.only_totals_per_day
        else:
            res["only_totals_per_day"] = False


        return res
    def _get_lines_per_day(self,docids,data):
        new_list = []
        used_taxes_list =self.env['account.tax']
        for move in self.env['account.move'].browse(docids):
            inv_taxes,used_taxes = self._get_tax_lines(move,data)
            used_taxes_list = used_taxes_list | used_taxes
            inv_taxes_new = []

            for tax in inv_taxes:
                elem = filter(lambda l: l['invoice_date'] == tax['invoice_date'] and l['tax_rec'].id ==tax['tax_rec'].id,new_list)
                elem = list(elem)
                if len(elem)==0:
                    new_list.append(tax)
                else:
                    new_list.remove(elem[0])

                    elem = elem[0]
                    elem.update({'base':(elem['base'] + tax['base']),'tax':(elem['tax'] + tax['tax']) })
                    new_list.append(elem)



        return new_list,used_taxes_list

    # @api.model
    # def _compute_totals_tax(self, tax, data):
    #     res = super()._compute_totals_tax(tax, data)
    #
    #     if tax.is_split_payment:
    #         # res = (tax_name, base, tax, deductible, undeductible)
    #         #
    #         # In case of SP tax, SP VAT must not appear as deductible.
    #         #
    #         return (res[0], res[1], res[2], 0.0, res[4])
    #
    #     return res
