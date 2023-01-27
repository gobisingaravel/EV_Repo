# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'
    _description = "Skill level for an employee"

    applicant_id = fields.Many2one('hr.applicant',required=False)
    employee_id = fields.Many2one('hr.employee',required=False)
    job_id = fields.Many2one('hr.job',required=False)
    country_master_id = fields.Many2one(
        'country.master', 'Country', tracking=True)


    _sql_constraints = [
        ('_unique_appl_skill', 'unique (applicant_id, skill_id)', "Two levels for the same skill is not allowed"),
    ]


class ResumeLine(models.Model):
    _inherit = 'hr.resume.line'
    _description = "Resumé line of an employee"

    applicant_id = fields.Many2one('hr.applicant',required=False)
    employee_id = fields.Many2one('hr.employee',required=False)
    country_master_id = fields.Many2one(
        'country.master', 'Country', tracking=True)

