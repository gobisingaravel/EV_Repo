# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

import requests
import json


class SupervisorMaster(models.Model):
    _name = 'supervisor.master'
    _description = 'Supervisor Master'

    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]


    name = fields.Char(string="Name")
    supervisorid = fields.Integer(string="Supervisor ID")
    user_id = fields.Many2one('res.users',string="User")
    user_ids = fields.Many2many('res.users', string="User")
    employee_id = fields.Many2one('hr.employee',string="User")


    def get_supervisor(self):
        userid = self._context.get('uid')
        user_obj = self.env['res.users'].sudo().browse(userid)
        token = user_obj.token
        url = "https://evox2.eastvantage.com/server/api/role/supervisor/users?page=all"
        headers = {
            'Authorization': 'Bearer' + str(token),
            'x-authorization': 'RlYVynDl9ALmOtfCotsLS9iSr93bMzgpIWfoxLktznLfTUL3NfaNO5HittoAfA9Z'}
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.content)
        supervisor_list = data.get('content')
        # print("supervisorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",len(supervisor_list))
        # for supervisor in supervisor_list:
        #     self.env.cr.execute('select s.id from supervisor_master as s where s.supervisorid = %s',
        #                         [supervisor.get('id')])
        #     supervisor_obj = self.env.cr.fetchall()
        #     if supervisor.get('supervisee'):
        #         self.env.cr.execute('select u.id from res_users as u where u.user_res_id = %s',
        #                             [supervisor.get('supervisee')[0].get('id')])
        #         user_obj = self.env.cr.fetchall()
        #         if user_obj:
        #             user_id = self.env['res.users'].browse(user_obj[0])
        #     else:
        #         continue
        #     if supervisor_obj:
        #         supervisor_id = self.env['supervisor.master'].browse(supervisor_obj[0])
        #         if user_obj:
        #             supervisor_id.user_ids = [(4, [user_id.id])]
        #     else:
        #         vals = {
        #                 'name': supervisor.get('full_name'),
        #                 'supervisorid':supervisor.get('id'),
        #             }
        #         supervisor_master_obj = self.env['supervisor.master'].sudo().create(vals)
        #         # if user_obj:
        #         #     supervisor_master_obj.user_ids = [(4, [user_id.id])]
        #

