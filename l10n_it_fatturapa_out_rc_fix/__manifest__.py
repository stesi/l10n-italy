# Copyright 2020 Lorenzo Battistini @ TAKOBI
# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Fix ITA - Emissione e-fattura con reverse charge",
    "summary": "Integrazione l10n_it_fatturapa_out e l10n_it_reverse_charge Fix",
    "version": "14.0.1",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Stesi",
    "maintainers": ["dirobertovincenzo"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        # "l10n_it_fatturapa_out",
        # "l10n_it_reverse_charge",
        # "l10n_it_fatturapa_out_rc",
        "l10n_it_fatturapa_out_semplificata",
    ],
    "data": [
        "views/invoice_it_template.xml"
    ],
}
