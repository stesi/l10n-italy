# -*- coding: utf-8 -*-
{
    'name': "Fatturapa out autofattura fornitore",





    'author': "STeSI srl",
    'website': "http://www.stesi.srl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.56',

    # any module necessary for this one to work correctly
    'depends': ['base', 'l10n_it_fatturapa_out'],

    # always loaded
    'data': [
        'data/invoice_it_template.xml',
        'views/partner_view.xml'

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
