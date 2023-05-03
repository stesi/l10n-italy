# -*- coding: utf-8 -*-
{
    'name': "Account Vat Period End STatement Custom",

    'summary': "Account Vat Period End STatement Custom",

    'license': 'OPL-1',

    'author': "STeSI Srl",

    'category': 'custom',

    'version': '14.0.0.1',

    'website': "http://www.stesi.eu",

    # any module necessary for this one to work correctly
    'depends': ['account_vat_period_end_statement'],

    # always loaded
    'data': ['views/report_vatperiodendstatement.xml'],

    'application': False,
}
