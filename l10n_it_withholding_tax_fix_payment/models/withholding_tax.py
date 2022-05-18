# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, fields, models


class WithholdingTaxStatement(models.Model):
    """
    The Withholding tax statement are created at the invoice validation
    """
    _inherit = "withholding.tax.statement"

    def get_wt_competence(self, amount_reconcile):
        dp_obj = self.env["decimal.precision"]
        amount_wt = 0
        for st in self:
            if st.invoice_id:
                domain = [
                    ("invoice_id", "=", st.invoice_id.id),
                    ("withholding_tax_id", "=", st.withholding_tax_id.id),
                ]
                wt_inv = self.env["account.invoice.withholding.tax"].search(
                    domain, limit=1
                )
                if wt_inv:
                    if st.invoice_id.amount_net_pay_residual > 0:
                        amount_wt = 0
                    else:
                        # Aggiunto per fixare il caso di pagamenti multipli

                        amount_base = st.invoice_id.amount_untaxed

                        base = round(amount_base * wt_inv.base_coeff, 5)
                        amount_wt = round(
                            base * wt_inv.tax_coeff, dp_obj.precision_get("Account")
                        )
                if st.invoice_id.move_type in ["in_refund", "out_refund"]:
                    amount_wt = -1 * amount_wt
            elif st.move_id:
                tax_data = st.withholding_tax_id.compute_tax(amount_reconcile)
                amount_wt = tax_data["tax"]
            return amount_wt
