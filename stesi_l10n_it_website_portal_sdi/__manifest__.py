#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - SDI - Portale",
    "summary": "Aggiunge SDI tra i dettagli dell'utente nel portale.",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA), STESI SRL",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa",
        "portal",
        "website_sale"
    ],
    "data": [
        'data/data.xml',
        "views/portal_templates.xml",
    ],
    "auto_install": True,
}
