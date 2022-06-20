# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Gestione Cespiti Stesi',
    'version': '14.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': "Gestione Cespiti",
    'author': 'Stesi',
    'website': 'https://gitlab.hubeditoriale.it/devis.meneghelli/odoo-14-asset-management',
    'license': 'AGPL-3',
    'depends': [
        'assets_management',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'development_status': 'Beta',
    'auto_install': True,
    'installable': True,
}
