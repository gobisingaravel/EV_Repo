# Part of Odoo. See LICENSE file for full copyright and licensing details.

import ast

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import json
import requests

# from pdfminer.high_level import extract_text


class Applicant(models.Model):
    _name = "hr.applicant"
    _inherit = ['hr.applicant','mail.thread.cc', 'mail.activity.mixin', 'utm.mixin']


    @api.depends('job_id')
    def _get_domain(self):
        users_list = []
        for user in self.job_id.job_owner_ids:
            users_list.append(user.id)
        if users_list:
            domain = [('id', 'in', users_list)]
        else:
            domain = lambda self: [("groups_id", "=", self.env.ref("hr_recruitment.group_hr_recruitment_user").id)]
        return domain


    resume_line_ids = fields.One2many('hr.resume.line', 'applicant_id', string="Resumé lines")
    employee_skill_ids = fields.One2many('hr.employee.skill', 'applicant_id', string="Skills")
    country_id = fields.Many2one(
        'res.country', 'Country', groups="hr.group_hr_user", tracking=True)
    client_id = fields.Many2one('res.users',string="Client",related="job_id.client_id",tracking=True, index=True,store=True)
    total_experience = fields.Char(string="Experience")
    notice_period = fields.Char(string="Notice period")
    current_ctc = fields.Float(string="Current CTC",digits=(12,2))
    salary_proposed = fields.Float("Proposed CTC", group_operator="avg", help="Salary Proposed by the Organisation",
                                   tracking=True,digits=(12,2))
    salary_expected = fields.Float("Expected CTC", group_operator="avg", help="Salary Expected by Applicant",
                                   tracking=True,digits=(12,2))
    current_role = fields.Char(string="Current Role")
    current_company = fields.Char(string="Current Company")
    current_location = fields.Char(string="Current Location")
    status = fields.Char(string="Status")
    resume_upload = fields.Binary("Upload Resume",attachment=True)
    availability = fields.Date("Interview Date", help="The date at which the applicant will be available to start working", tracking=True)
    exam_date = fields.Date("Exam Date", tracking=True)
    endorsed_date = fields.Date("Endorsed Date", tracking=True)
    user_ids = fields.Many2many('res.users', "Recruiters",related="job_id.job_team_ids")
    user_recruiter_id = fields.Many2one(
        'res.users', "Recruiter",domain=lambda self: [("groups_id", "=",self.env.ref("hr_recruitment.group_hr_recruitment_user").id)],
        tracking=True, readonly=False)
    phone_calling_code = fields.Integer(string="ISD Code",related="country_id.phone_code")
    designation_id = fields.Many2one('designation.master', string="Designation")
    client_master_id = fields.Many2one('client.master', string="Client",related="job_id.client_master_id",tracking=True, index=True,store=True)
    country_master_id = fields.Many2one(
        'country.master', 'Country', tracking=True)



    @api.model_create_multi
    def create(self, vals_list):
        res = super(Applicant, self).create(vals_list)
        resume_lines_values = []
        for employee in res:
            line_type = self.env.ref('hr_skills.resume_type_experience', raise_if_not_found=False)
            resume_lines_values.append({
                'applicant_id': employee.id or '',
                'name': employee.company_id.name or '',
                'date_start': employee.create_date.date(),
                'description': employee.job_id.name or '',
                'line_type_id': line_type and line_type.id,
            })
        self.env['hr.resume.line'].create(resume_lines_values)
        return res


    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'type': 'private',
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                applicant.partner_id = new_partner_id
                address_id = new_partner_id.address_get(['contact'])['contact']

            skill_result = []
            for line in applicant.employee_skill_ids:
                skill_result.append((0, 0, {'skill_type_id': line.skill_type_id.id, 'skill_level_id': line.skill_level_id.id,
                                            'skill_id': line.skill_id.id, 'level_progress': line.level_progress}))

            resume_result = []
            for line in applicant.resume_line_ids:
                resume_result.append(
                    (0, 0, {'name':line.name,
                            'line_type_id': line.line_type_id.id, 'date_start': line.date_start,
                            'display_type': line.display_type, 'date_end': line.date_end}))

            if applicant.partner_name or contact_name:
                employee_data = {
                    'default_name': applicant.partner_name or contact_name,
                    'default_job_id': applicant.job_id.id,
                    'default_job_title': applicant.job_id.name,
                    'default_address_home_id': address_id,
                    'default_department_id': applicant.department_id.id or False,
                    'default_address_id': applicant.company_id and applicant.company_id.partner_id
                                          and applicant.company_id.partner_id.id or False,
                    'default_work_email': applicant.department_id and applicant.department_id.company_id
                                          and applicant.department_id.company_id.email or False,
                    'default_work_phone': applicant.department_id.company_id.phone,
                    'default_country_id': applicant.country_id.id or False,
                    'form_view_initial_mode': 'edit',
                    'default_applicant_id': applicant.ids,
                    'default_employee_skill_ids': skill_result,
                    'default_resume_line_ids': resume_result,
                    # 'default_applicant_id': applicant.id,
                }

        dict_act_window = self.env['ir.actions.act_window']._for_xml_id('hr.open_view_employee_list')
        dict_act_window['context'] = employee_data
        return dict_act_window