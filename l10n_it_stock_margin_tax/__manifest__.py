# -*- coding: utf-8 -*-
{
    'name': "Tax margin on stock",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",



    'author': "STeSI srl",
    'website': "http://www.stesi.srl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['stock','l10n_it_account_margin_tax'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking.xml',
        'views/stock_production_lot.xml',
        # 'data/automated_action.xml'
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
