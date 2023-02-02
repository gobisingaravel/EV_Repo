# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import json

class ResUsers(models.Model):
    _inherit = 'res.users'

    token = fields.Char(string="Token")
    user_res_id = fields.Integer(string="ID")
    date_hired = fields.Date(string="Date Hired")
    termination_date = fields.Date(string="Termination Date")
    employee_num = fields.Char(string="Employee Number")
    bhr_num = fields.Char(string="Bhr Num")
    dpa_ticket_at = fields.Datetime(string="DPA Ticket")
    nick_name = fields.Char(string="Nick Name")
    employment_status_id = fields.Many2one('status.master', string="Employment Status")
    designation_id = fields.Many2one('designation.master', string="Designation")
    created_date = fields.Datetime(string="Created at")
    updated_date = fields.Datetime(string="Updated at")
    deleted_date = fields.Datetime(string="Deleted at")
    force_change_pwd = fields.Boolean(string="Force Change Password")
    supervisor_master_id = fields.Many2one('supervisor.master',string="Supervisor")
    country_master_id = fields.Many2one('country.master',string="Country")



    def get_users(self):
        userid = self._context.get('uid')
        user_obj = self.env['res.users'].sudo().browse(userid)
        token = user_obj.token
        uid = user_obj.user_res_id
        url = "https://evox2.eastvantage.com/server/api/department/all"
        headers = {
            'Authorization': 'Bearer' + str(token),
            'x-authorization': 'RlYVynDl9ALmOtfCotsLS9iSr93bMzgpIWfoxLktznLfTUL3NfaNO5HittoAfA9Z'}
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.content)
        user_list = data.get('content')
        for user in user_list:
            self.env.cr.execute('select u.id from res_users as u where u.user_res_id = %s', [user.get('id')])
            usr = self.env.cr.fetchall()
            if not usr:
                vals = {
                    'name': user.get('name'),
                    'user_res_id':user.get('id'),
                }
                user_obj_id = self.env['res.users'].sudo().create(vals)
                # user_obj_id.action_create_employee()



    # def action_create_employee(self):
    #     self.ensure_one()
    #     self.env['hr.employee'].create(dict(
    #         name=self.name,
    #         company_id=self.env.company.id,
    #         **self.env['hr.employee']._sync_user(self)
    #     ))

