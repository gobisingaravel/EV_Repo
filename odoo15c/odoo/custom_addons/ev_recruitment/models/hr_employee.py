# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee"


    applicant_id = fields.Many2one('hr.applicant',string="Applicant")
    client_master_id = fields.Many2one('client.master',string="Client")
    country_master_id = fields.Many2one(
        'country.master', 'Country', tracking=True)