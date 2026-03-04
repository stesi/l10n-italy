from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    doi_type = fields.Selection(
        [("in", "Issued from company"), ("out", "Received from customers")],
        compute="_compute_l10n_it_edi_doi_type",
    )

    @api.depends("move_type")
    def _compute_l10n_it_edi_doi_type(self):
        purchase_types = self.env["account.move"].get_purchase_types()
        sale_types = self.env["account.move"].get_sale_types()
        for move in self:
            if move.move_type in purchase_types:
                move.doi_type = "in"
            elif move.move_type in sale_types:
                move.doi_type = "out"
            else:
                move.doi_type = False

    def _compute_l10n_it_edi_doi_use(self):
        purchase_move_ids = self.filtered(lambda x: x.doi_type == "in")
        other_move_ids = self - purchase_move_ids
        super(AccountMove, other_move_ids)._compute_l10n_it_edi_doi_use()
        for move in purchase_move_ids:
            move.l10n_it_edi_doi_use = (
                move.l10n_it_edi_doi_id or move.country_code == "IT"
            )
        return  # W8110

    def _compute_l10n_it_edi_doi_amount(self):
        purchase_move_ids = self.filtered(lambda x: x.doi_type == "in")
        other_move_ids = self - purchase_move_ids
        super(AccountMove, other_move_ids)._compute_l10n_it_edi_doi_amount()
        for move in purchase_move_ids:
            l10n_it_edi_doi_bill_tax_ids = move.company_id.l10n_it_edi_doi_bill_tax_id
            if not l10n_it_edi_doi_bill_tax_ids or not move.l10n_it_edi_doi_id:
                move.l10n_it_edi_doi_amount = 0
                continue
            declaration_lines = move.invoice_line_ids.filtered(
                lambda line,
                l10n_it_edi_doi_bill_tax_ids=l10n_it_edi_doi_bill_tax_ids: all(
                    tax in line.tax_ids for tax in l10n_it_edi_doi_bill_tax_ids
                )
            )
            move.l10n_it_edi_doi_amount = sum(declaration_lines.mapped("price_total"))
        return  # W8110

    def _compute_l10n_it_edi_doi_id(self):
        purchase_move_ids = self.filtered(lambda x: x.doi_type == "in")
        other_move_ids = self - purchase_move_ids
        super(AccountMove, other_move_ids)._compute_l10n_it_edi_doi_id()
        for move in purchase_move_ids:
            if not move.l10n_it_edi_doi_use or (
                move.state != "draft" and not move.l10n_it_edi_doi_id
            ):
                move.l10n_it_edi_doi_id = False
                continue

            partner = move.partner_id.commercial_partner_id
            validity_warnings = move.l10n_it_edi_doi_id._get_validity_warnings(
                move.company_id, partner, move.currency_id, move.l10n_it_edi_doi_date
            )
            if move.l10n_it_edi_doi_id and not validity_warnings:
                continue

            declaration = self.env[
                "l10n_it_edi_doi.declaration_of_intent"
            ]._fetch_valid_declaration_of_intent(
                move.company_id,
                partner,
                move.currency_id,
                move.l10n_it_edi_doi_date,
                doi_type="in",
            )
            move.l10n_it_edi_doi_id = declaration
        return  # W8110

    def _post(self, soft=True):
        errors = []
        for move in self:
            declaration = move.l10n_it_edi_doi_id
            doi_bill_tax = move.company_id.l10n_it_edi_doi_bill_tax_id
            if not doi_bill_tax:
                continue
            declaration_lines = move.invoice_line_ids.filtered(
                lambda line, doi_bill_tax=doi_bill_tax: doi_bill_tax in line.tax_ids
            )
            if declaration_lines and not declaration:
                errors.append(
                    _(
                        "Given the tax %s is applied, there should be a "
                        "Declaration of Intent selected.",
                        doi_bill_tax.name,
                    )
                )

        if errors:
            raise UserError("\n".join(errors))
        return super()._post(soft)
