# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
import tempfile
import binascii
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, _
import logging
_logger = logging.getLogger(__name__)
import io
try:
	import xlrd
except ImportError:
	_logger.debug('Cannot `import xlrd`.')
try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import xlwt
except ImportError:
	_logger.debug('Cannot `import xlwt`.')
try:
	import cStringIO
except ImportError:
	_logger.debug('Cannot `import cStringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')


class ImportHrApplicants(models.TransientModel):
	_name = "import.hr.applicants"
	_description = "Applicants"


	file_select = fields.Binary(string="Select File")
	import_option = fields.Selection([('csv', 'CSV File'),('xls', 'XLS File')],string='Select',default='csv')

	
	def imoport_file(self):
		if self.import_option == 'csv':
			keys = ['partner_name', 'name']
			try:
				csv_data = base64.b64decode(self.file_select)
				data_file = io.StringIO(csv_data.decode("utf-8"))
				data_file.seek(0)
				file_reader = []
				values = {}
				csv_reader = csv.reader(data_file, delimiter=',')
				file_reader.extend(csv_reader)

			except:
				raise UserError(_("Invalid file!"))

			for i in range(len(file_reader)):
				field = list(map(str, file_reader[i]))
				values = dict(zip(keys, field))
				if values:
					if i == 0:
						continue
					else:
						values.update({
										'create_date':field[0],
										'status': field[1],
										'description': field[2],
										'partner_name' : field[3],
										'job_id': field[4],
										'client_id':field[5],
										'email':field[6],
										'partner_phone': field[7],
										'partner_mobile': field[7],
										'source_id' : field[8],
										'experience':field[9],
										'current_ctc': field[10],
										'salary_expected': field[11],
										'current_company': field[12],
										'current_role': field[13],
										'current_location': field[14],
										'notice_period': field[15],
										})
						res = self.create_applicants(values)

		elif self.import_option == 'xls':
			try:
				fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
				fp.write(binascii.a2b_base64(self.file_select))
				fp.seek(0)
				import xlrd
				values = {}
				workbook = xlrd.open_workbook(fp.name)
				sheet = workbook.sheet_by_index(0)

			except:
				raise UserError(_("Invalid file!"))

			print("==========================",sheet.nrows)
			for row_no in range(sheet.nrows):
				val = {}
				if row_no <= 0:
					fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
				else:

					line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))

					values.update( {'create_date':line[0],
										'status': line[1],
										'description': line[2],
										'partner_name' : line[3],
										'job_id': line[4],
										'client_id':line[5],
										'email':line[6],
										'partner_phone': line[7],
										'partner_mobile': line[7],
										'source_id' : line[8],
										'experience':line[9],
										'current_ctc': line[10],
										'salary_expected': line[11],
										'current_company': line[12],
										'current_role': line[13],
										'current_location': line[14],
										'notice_period': line[15] or False,
									})

					res = self.create_applicants(values)
		else:
			raise UserError(_("Please select any one from xls or csv formate!"))

		return res
	

	def create_applicants(self,values):
		applicant_obj = self.env['hr.applicant']
		job_get = self.find_job(values.get('job_id'))
		# stage = self.get_stage(values.get('stage_id'))
		client = self.get_client(values.get('client_id'))
		source = self.get_source(values.get('source_id'))
		if values.get('current_role') and values.get('experience'):
			name = values.get('current_role') + " of " + str(values.get('experience')) + " experience"
		else:
			name = "Fresher"

		data={
			'create_date': values.get('create_date'),
			'status': values.get('status'),
			'description': values.get('description'),
			'partner_name': values.get('partner_name'),
			'job_id': job_get or False,
			'client_id': client or False,
			'email_from': values.get('email'),
			'partner_phone': values.get('partner_phone'),
			'partner_mobile': values.get('partner_mobile'),
			'source_id': source or False,
			'total_experience': values.get('experience'),
			'current_ctc': values.get('current_ctc'),
			'salary_expected': values.get('salary_expected'),
			'current_company': values.get('current_company'),
			'current_role': values.get('current_role'),
			'current_location': values.get('current_location'),
			'notice_period': values.get('notice_period'),
			'name' : name,
			# 'stage_id': stage or False,
				}
		applicant_id = applicant_obj.create(data)
		return applicant_id


	def find_job(self, name):
		job_obj = self.env['hr.job']
		job_id = job_obj.search([('name', '=', name)])
		if job_id:
			return job_id.id
		else:
			if name == "":
				pass
			else:
				job = self.env['hr.job'].create({'name': name})
				return job.id
				# raise UserError(_(' %s Job Position is not available.') % name)


	def get_client(self, name):
		client_obj = self.env['res.users']
		client_id = client_obj.search([('name', '=', name)])
		if client_id:
			return client_id.id
		else:
			if name == "":
				pass
			else:
				client = self.env['res.users'].create({'name': name})
				return client.id
				# raise UserError(_(' %s Job Position is not available.') % name)


	def get_source(self, name):
		source_obj = self.env['utm.source']
		source_id = source_obj.search([('name', '=', name)])
		if source_id:
			return source_id.id
		else:
			if name == "":
				pass
			else:
				source = self.env['utm.source'].create({'name': name})
				return source.id
				# raise UserError(_(' %s Job Position is not available.') % name)


	def get_stage(self, name):
		stage_obj = self.env['hr.recruitment.stage']
		stage_id = stage_obj.search([('name', '=', name)])
		if stage_id:
			return stage_id.id
		else:
			if name == "":
				pass
			else:
				stage = self.env['hr.recruitment.stage'].create({'name': name})
				return stage.id