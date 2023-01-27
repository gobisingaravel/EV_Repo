# -*- coding: utf-8 -*-
#############################################################################
#

#
#############################################################################

{
    'name': 'Customize Login Page Style',
    'version': '15.0.1.0.0',
    'summary': 'Customize The Login Page With Different Styles',
    'description': 'Customize The Login Page With Different Styles',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'base_setup',
        'web',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/webclient_templates_right.xml',
        'views/webclient_templates_left.xml',
        'views/webclient_templates_middle.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
