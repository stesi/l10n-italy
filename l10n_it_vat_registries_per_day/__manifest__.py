# -*- coding: utf-8 -*-
{
    'name': "Vat registry per day",


    'license': 'OPL-1',

    'author': "STeSI Srl",

    'category': 'Custom',

    'version': '14.0.0.1',

    'website': "http://www.stesi.eu",

    # any module necessary for this one to work correctly
    'depends': ['l10n_it_vat_registries'],

    # always loaded
    'data': ['report/report_registro_iva.xml','wizard/print_registro_iva.xml'],

    'application': True,
}
