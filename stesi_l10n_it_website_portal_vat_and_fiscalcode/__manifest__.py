#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Vat And Fiscalcode - Portale",
    "summary": "Aggiunge l'indice Fiscalcode e Vat tra i dettagli dell'utente nel portale.",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA), STESI SRL",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fiscalcode",
        "portal",
        "website_sale"
    ],
    "data": [
        'data/data.xml',
        "views/portal_templates.xml",
    ],
    'pre_init_hook': '_pre_init_check_module',
    "auto_install": True,
}
