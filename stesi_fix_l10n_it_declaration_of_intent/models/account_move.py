from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_declaration_residual_amounts(self, declarations):
        """Get residual amount for every `declarations`."""
        declarations_amounts = {}
        # If the tax amount is 0, then there is no line representing the tax
        # so there will be no line having tax_line_id.
        # Therefore we choose instead the lines that
        # should generate the tax line i.e. the lines that have `tax_ids`
        tax_lines = self.line_ids.filtered("tax_ids")
        for tax_line in tax_lines:
            # Move lines having `tax_ids` represent the base amount for those taxes
            amount = tax_line.price_subtotal
            for declaration in declarations:
                if declaration.id not in declarations_amounts:
                    declarations_amounts[declaration.id] = declaration.available_amount
                if any(tax in declaration.taxes_ids for tax in tax_line.tax_ids):
                    if tax_line.move_id.move_type not in ['in_refund']:
                        declarations_amounts[declaration.id] -= amount
                    else:
                        declarations_amounts[declaration.id] += amount
        for declaration in declarations:
            # exclude amount from lines with invoice_id equals to self
            for line in declaration.line_ids.filtered(lambda l: l.invoice_id == self):
                declarations_amounts[declaration.id] += line.amount
        return declarations_amounts


