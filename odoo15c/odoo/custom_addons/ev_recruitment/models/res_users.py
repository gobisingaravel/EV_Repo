# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class Users(models.Model):
    _inherit = "res.users"


    job_count = fields.Integer('Total Job Positions',compute="get_job_count",readonly="1")
    ongoing_job_pos_count = fields.Integer('Ongoing Job Positions', compute="get_job_count", readonly="1")
    job_id = fields.Many2one('hr.job',string="Job Position")
    client_stage = fields.Selection([
        ('prospect', 'Prospect'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')], string='Stage')

    applicant_ids = fields.One2many('hr.applicant','client_id',string="Applicants")
    job_ids = fields.One2many('hr.job', 'client_id', string="Job Positions")
    department_id = fields.Many2one('hr.department',string="Industry")
    client_owner_ids = fields.Many2many('res.users','rel_client_user','activity_user_id','user_id', string="Client Owner",domain=lambda self: [("groups_id", "=",self.env.ref("hr_recruitment.group_hr_recruitment_manager").id)])
    client_team_ids = fields.Many2many('res.users','rel_team_user','user_id','activity_user_id', string="Recruiter",domain=lambda self: [("groups_id", "=",self.env.ref("hr_recruitment.group_hr_recruitment_user").id)])
    compute_field = fields.Boolean(string="check field", compute='get_user')
    country_master_id = fields.Many2one(
        'country.master', 'Country', tracking=True)


    @api.depends('compute_field')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self.id)])
        if res_user.has_group('ev_recruitment.group_hr_recruitment_client_own_documents'):
            self.compute_field = True
        else:
            self.compute_field = False


    def get_job_count(self):
        read_group_result = self.env['hr.job'].read_group([('client_id', 'in', self.ids)], ['client_id'], ['client_id'])
        result = dict((data['client_id'][0], data['client_id_count']) for data in read_group_result)
        read_group_result_job = self.env['hr.job'].read_group([('client_id', 'in', self.ids),('state','=','recruit')], ['client_id'], ['client_id'])
        result1 = dict((data['client_id'][0], data['client_id_count']) for data in read_group_result_job)
        for user in self:
            user.job_count = result.get(user.id, 0)
            user.ongoing_job_pos_count = result1.get(user.id, 0)


