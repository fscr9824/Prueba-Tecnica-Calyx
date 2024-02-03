# -*- coding: utf-8 -*-
{
    'name': "calyx_prueba_tecnica",

    'summary': """
        Prueba Tecnica""",

    'description': """
    """,

    'author': "Freddy Castillo",


    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        "data/data.xml",
        "views/sale_chanel.xml",
        "views/sale_order.xml",
        "views/credit_group.xml",
        "views/res_partner.xml",
        "wizard/wizard_credit_group.xml",
    ],
}
