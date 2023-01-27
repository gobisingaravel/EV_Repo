# -*- coding: utf-8 -*-
{
	'name': 'Import Applicants from CSV or Excel File',
	'version': '15.0.0.1',
	'category': 'Recruitment',
	'summary': 'This apps helps to import applicants using CSV or Excel file',
	'description': '''Using this module applicants is imported using excel sheets
	import applicants using csv 
	import applicants using xls
	import applicants using excel
	''',
	'author': 'Dayana Benny',
	'depends': ['base','hr_recruitment'],
	'data': [
		'security/ir.model.access.csv',
		'wizard/view_import_applicants.xml',
		],
	'auto_install': False,
	'installable': True,
    'application': True,
    'qweb': [
    		],}

