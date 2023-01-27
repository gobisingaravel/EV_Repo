# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class LocationMaster(models.Model):
    _name = 'location.master'
    _description = 'Location Master'

    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]


    name = fields.Char(string="Name")

    def get_location(self):
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
        locations_list = data.get('content')
        self.env.cr.execute('select l.id from location_master as l where l.name = %s', (data['Name']))
        desig = self.env.cr.fetchall()
        if not desig:
            vals= {
                'name': data['Name'],
            }
            self.env['location.master'].sudo().create(vals)

