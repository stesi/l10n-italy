# -*- coding: utf-8 -*-
{
    'name': "Margin account tax on pos lines",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",



    'author': "STeSI srl",
    'website': "http://www.stesi.srl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.8',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale','l10n_it_account_margin_tax','l10n_it_stock_margin_tax'],

    # always loaded
    'data': [
        'views/pos_order_line.xml',
        'data/base_automation.xml'

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
