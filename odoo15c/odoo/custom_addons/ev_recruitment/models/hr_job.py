# Part of Odoo. See LICENSE file for full copyright and licensing details.

import ast

from odoo import api, fields, models, _


class Job(models.Model):
    _inherit = "hr.job"
    # _inherit = ['hr.job', 'website.published.multi.mixin','mail.alias.mixin']
    _order = "sequence, state desc, name asc"

    client_master_id = fields.Many2one('client.master', string="Client")
    client_id = fields.Many2one('res.users',string="Client",related="client_master_id.user_id",tracking=True, index=True,store=True)
    turn_around_time = fields.Date(string="Turn Around Time")
    min_salary = fields.Float(string="Minimum Salary")
    max_salary = fields.Float(string="Maximum Salary")
    jobowner_id = fields.Many2one('res.users',string="Job Owner/POC",domain=lambda self: [("groups_id", "=", self.env.ref( "hr_recruitment.group_hr_recruitment_manager" ).id)])
    employee_skill_ids = fields.One2many('hr.employee.skill', 'job_id', string="Skills Required")
    user_id = fields.Many2one('res.users', "Recruiter", tracking=True,domain=lambda self: [("groups_id", "=",self.env.ref("hr_recruitment.group_hr_recruitment_user").id)])
    head_count = fields.Char(string="Head Count",compute="head_count_cal")
    job_team_ids = fields.Many2many('res.users', string="Recruiter",related="client_id.client_team_ids")
    job_owner_ids = fields.Many2many('res.users','rel_job_user','user_id','job_id', string="Job Owner",related="client_id.client_owner_ids")
    designation_id = fields.Many2one('designation.master',string="Designation")
    country_master_id = fields.Many2one(
        'country.master', 'Country', tracking=True)
    location_master_id = fields.Many2one(
        'location.master', 'Location', tracking=True)




    @api.depends('no_of_recruitment','all_application_count')
    def head_count_cal(self):
        for job in self:
            job.head_count = str(job.all_application_count) + " - " + str(job.no_of_recruitment)

