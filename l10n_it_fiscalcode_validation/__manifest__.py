# -*- coding: utf-8 -*-
{
    'name': "Fiscalcode validation",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",



    'author': "STeSI srl",
    'website': "http://www.stesi.srl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','l10n_it_fiscalcode'],
    "external_dependencies": {
        "python": ["python-slugify","python-fsutil"],
    },
    # always loaded
    'data': [

        # 'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
