# -*- coding: utf-8 -*-
{
    'name': "l10n_it_fatturapa_out_custom_codicetipo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",



    'author': "Stesi",
    'website': "http://www.stesi.srl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','l10n_it_fatturapa_out'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move.xml',
        'views/invoice_it_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
