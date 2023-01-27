# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import json

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    department_id = fields.Integer(string="ID")


    def get_department(self):
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
        dept_list = data.get('content')
        for dept in dept_list:
            self.env.cr.execute('select d.id from hr_department as d where d.department_id = %s', [dept.get('id')])
            dep = self.env.cr.fetchall()
            if not dep:
                vals = {
                    'name': dept.get('department_name'),
                    'department_id':dept.get('id'),
                }
                self.env['hr.department'].sudo().create(vals)

