import logging

_logger = logging.getLogger(__name__)

from odoo import models, fields, api

from odoo.addons.l10n_it_intrastat.models.account import AccountMove as OdooAccountMove


def _get_intrastat_lines_to_split(self):
    self.ensure_one()
    i_line_by_code = {}
    lines_to_split = []
    for line in self.invoice_line_ids:
        # Lines to compute
        if not line.product_id:
            continue
        product_template = line.product_id.product_tmpl_id

        intrastat_origin_country_id = self.env["res.country"].browse()

        if not product_template.intrastat_origin_country_id:
            if self.move_id.is_sale_document():
                intrastat_origin_country_id = self.move_id.company_id.partner_id.country_id
            elif self.move_id.is_purchase_document():
                intrastat_origin_country_id = self.move_id.partner_id.country_id
        else:
            intrastat_origin_country_id = self.product_id.intrastat_origin_country_id

        intrastat_data = product_template.get_intrastat_data()
        if (
            "intrastat_code_id" not in intrastat_data
            or intrastat_data["intrastat_type"] == "exclude"
        ):
            continue
        # Free lines
        if self.company_id.intrastat_exclude_free_line and not line.price_subtotal:
            continue
        # line to split
        if intrastat_data["intrastat_type"] == "misc":
            lines_to_split.append(line)
            continue
        if not intrastat_data["intrastat_code_id"]:
            continue

        # Group by intrastat code
        intra_line = line._prepare_intrastat_line()
        i_code_id = intra_line["intrastat_code_id"]
        i_code_type = intra_line["intrastat_code_type"]

        if int(str(f'{intrastat_origin_country_id.id}{i_code_id}')) in i_line_by_code:
            i_line_by_code[i_code_id]["amount_currency"] += intra_line[
                "amount_currency"
            ]
            i_line_by_code[i_code_id]["statistic_amount_euro"] += intra_line[
                "statistic_amount_euro"
            ]
            i_line_by_code[i_code_id]["weight_kg"] += intra_line["weight_kg"]
            i_line_by_code[i_code_id]["additional_units"] += intra_line[
                "additional_units"
            ]
        else:
            intra_line["statement_section"] = self.env[
                "account.invoice.intrastat"
            ].compute_statement_section(i_code_type, self.move_type)
            i_line_by_code[int(str(f'{intrastat_origin_country_id.id}{i_code_id}'))] = intra_line
    return i_line_by_code, lines_to_split


OdooAccountMove._get_intrastat_lines_to_split = _get_intrastat_lines_to_split


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _prepare_intrastat_line_country_good_origin(self, res):
        self.ensure_one()
        country_good_origin_id = self.env["res.country"].browse()
        if not self.product_id.intrastat_origin_country_id:
            if self.move_id.is_sale_document():
                country_good_origin_id = self.move_id.company_id.partner_id.country_id
            elif self.move_id.is_purchase_document():
                country_good_origin_id = self.move_id.partner_id.country_id
        else:
            country_good_origin_id = self.product_id.intrastat_origin_country_id
        res.update({"country_good_origin_id": country_good_origin_id.id})

    def _prepare_intrastat_line_country_origin(self, res):
        self.ensure_one()
        country_origin_id = self.env["res.country"].browse()
        if not self.product_id.intrastat_origin_country_id:
            if self.move_id.is_sale_document():
                country_origin_id = self.move_id.company_id.partner_id.country_id
            elif self.move_id.is_purchase_document():
                country_origin_id = self.move_id.partner_id.country_id
        else:
            country_origin_id = self.product_id.intrastat_origin_country_id
        res.update({"country_origin_id": country_origin_id.id})
