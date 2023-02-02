# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Meeting Rooms",
    'category': 'Meeting Rooms',
    'version': '1.3',
    'summary': "Manage meetings",
    'description': """
Create meeting rooms for your event.
    """,
    'depends': ['base_setup', 'mail', 'portal', 'utm','calendar','masters'],
    'data': [
        'security/ir.model.access.csv',
        'data/groups.xml',
        'data/system_parameter.xml',
        'data/data.xml',
        'data/mail_template.xml',
        'views/meeting_rooms_view.xml',
        'views/meeting_office_view.xml',
        'views/transactions_view.xml',
        'views/available_access_view.xml',
        'views/meeting_view.xml',
        'views/required_items_view.xml',
        # 'views/country_master_view.xml',
        'views/menu_views.xml',
        'wizard/meeting_booked_wizard.xml',
    ],
    'license': 'LGPL-3',
}
