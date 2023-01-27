# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Ev Recruitment',
    'version': '1.0',
    'category': 'Recruitment',
    'author':'Dayana Benny',
    'sequence': 90,
    'summary': 'Ev Recruitment Customization',
    'description': "",
    'website': 'https://www.odoo.com/app/recruitment',
    'depends': [
        'hr_recruitment','hr','hr_skills','web_search_with_and','website_hr_recruitment','masters'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/job_position_report.xml',
        'report/job_position_report_templates.xml',
        'data/config_data.xml',
        'data/hr_recruitment_data.xml',
        'views/hr_job_views.xml',
        'views/hr_applicant_views.xml',
        'views/res_company_views.xml',
        'views/hr_employee_views.xml',
        'views/new_hire_applicant.xml',
        'views/client_users_view.xml',
        'views/website_hr_recruitment_templates.xml',
        'views/menu_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'website.assets_editor': [
            'website_hr_recruitment/static/src/js/**/*',
        ],
    },
    'license': 'LGPL-3',
}
