# -*- coding: utf-8 -*-
{
    'name': "ITA - Termini fiscali di pagamento obbligatori",

    'summary': "Rende obbligatorio il campo termine di pagamento nella fattura",

    'license': 'OPL-1',

    'author': "STeSI Srl",

    'category': '',

    'version': '14.0.0.1',

    'website': "http://www.stesi.eu",

    # any module necessary for this one to work correctly
    'depends': ['l10n_it_fiscal_payment_term'],

    # always loaded
    'data': [
        'views/account_views.xml',
    ],

    'application': False,
}
