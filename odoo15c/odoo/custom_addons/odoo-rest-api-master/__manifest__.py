# -*- coding: utf-8 -*-
{
    'name': "Odoo REST API",

    'summary': """
        Odoo REST API""",

    'description': """
        Odoo REST API
    """,


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'developers',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','masters'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],

    "application": True,
    "installable": True,
    "auto_install": False,

    # 'external_dependencies': {
    #     'python': ['pypeg2']
    # }
}