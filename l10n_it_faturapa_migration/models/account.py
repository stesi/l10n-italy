# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2019 Lorenzo Battistini <https://github.com/eLBati>
from odoo import api, fields, models

class FaturapaActivityProgress(models.Model):
    # _position = ['2.1.7']
    _name = "faturapa.activity.progress"
    _description = "E-invoice activity progress"

    fatturapa_activity_progress = fields.Integer("Activity Progress")
    invoice_id = fields.Many2one(
        "account.move", "Related Invoice", ondelete="cascade", index=True
    )


class FaturapaSummaryData(models.Model):
    # _position = ['2.2.2']
    _name = "faturapa.summary.data"
    _description = "E-invoice summary data"
    tax_rate = fields.Float("Tax Rate")
    non_taxable_nature = fields.Selection(
        [
            ("N1", "excluded pursuant to Art. 15"),
            ("N2", "not subject"),
            (
                "N2.1",
                "not subject to VAT under the articles from 7 to "
                "7-septies of DPR 633/72",
            ),
            ("N2.2", "not subject – other cases"),
            ("N3", "not taxable"),
            ("N3.1", "not taxable – exportations"),
            ("N3.2", "not taxable – intra Community transfers"),
            ("N3.3", "not taxable – transfers to San Marino"),
            ("N3.4", "not taxable – transactions treated as export supplies"),
            ("N3.5", "not taxable – for declaration of intent"),
            (
                "N3.6",
                "not taxable – other transactions that don’t contribute to the "
                "determination of ceiling",
            ),
            ("N4", "exempt"),
            ("N5", "margin regime"),
            ("N6", "reverse charge"),
            (
                "N6.1",
                "reverse charge – transfer of scrap and of other recyclable "
                "materials",
            ),
            ("N6.2", "reverse charge – transfer of gold and pure silver"),
            ("N6.3", "reverse charge – subcontracting in the construction sector"),
            ("N6.4", "reverse charge – transfer of buildings"),
            ("N6.5", "reverse charge – transfer of mobile phones"),
            ("N6.6", "reverse charge – transfer of electronic products"),
            (
                "N6.7",
                "reverse  charge – provisions in the construction and related "
                "sectors",
            ),
            ("N6.8", "reverse charge – transactions in the energy sector"),
            ("N6.9", "reverse charge – other cases"),
            ("N7", "VAT paid in other EU countries"),
        ],
        string="Non taxable nature",
    )
    incidental_charges = fields.Float("Incidental Charges")
    rounding = fields.Float("Rounding")
    amount_untaxed = fields.Float("Amount Untaxed")
    amount_tax = fields.Float("Amount Tax")
    payability = fields.Selection(
        [
            ("I", "Immediate payability"),
            ("D", "Deferred payability"),
            ("S", "Split payment"),
        ],
        string="VAT payability",
    )
    law_reference = fields.Char("Law reference", size=128)
    invoice_id = fields.Many2one(
        "account.move", "Related Invoice", ondelete="cascade", index=True
    )
