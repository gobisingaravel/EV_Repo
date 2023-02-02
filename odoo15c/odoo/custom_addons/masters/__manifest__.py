# -*- coding: utf-8 -*-
{
    'name': "Masters",

    'summary': """ """,
    'description': """
    """,

    'author': "Dayana Benny",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','hr','hr_timesheet','project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/client_views.xml',
        'views/country_master_view.xml',
        'views/designation_views.xml',
        'views/user_creation_from_employee_view.xml',
        'views/views.xml',
        'views/location_views.xml',
        'views/employment_status_views.xml',
        'views/evox_view.xml',
        'views/department_view.xml',
        'views/supervisor_views.xml',
        # 'views/webclient_templates.xml',

        # 'views/res_config_settings_views.xml',
        # 'views/webclient_templates_right.xml',
        # 'views/webclient_templates_left.xml',
        # 'views/webclient_templates_middle.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
