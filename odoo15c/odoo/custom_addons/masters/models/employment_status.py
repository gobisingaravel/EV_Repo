# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class EmploymentStatusMaster(models.Model):
    _name = 'status.master'
    _description = 'Employment Status Master'

    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]


    name = fields.Char(string="Name")
    status_id = fields.Char(string="Status ID")
    status_code = fields.Char(string="Status Code")
    is_active = fields.Boolean(string="Is Active")
    modified_on_date = fields.Datetime(string="Modified On")


    def get_status(self):
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
        status_list = data.get('content')
        self.env.cr.execute('select s.id from status_master as s where s.name = %s and s.status_code = %s', (data['StatusName'],data['StatusCode']))
        status = self.env.cr.fetchall()
        if not status:
            vals= {
                'name': data['StatusName'],
                'status_id':data['StatusId'],
                'status_code':data['StatusCode'],
                'create_date': data['CreatedOn'],
                'modified_on_date': data['ModifiedOn'],
                'is_active': data['IsActive'],
                'create_uid': data['CreatedBy'] or False,
            }
            self.env['status.master'].sudo().create(vals)

