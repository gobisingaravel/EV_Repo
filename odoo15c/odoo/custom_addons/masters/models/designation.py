# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import json


class DesignationMaster(models.Model):
    _name = 'designation.master'
    _description = 'Designation Master'

    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]


    name = fields.Char(string="Name")
    designation_id = fields.Char(string="Designation ID")
    designation_code = fields.Char(string="Designation Code")
    is_active = fields.Boolean(string="Is Active")
    modified_on_date = fields.Datetime(string="Modified On")


    def get_designation(self):
        userid = self._context.get('uid')
        user_obj = self.env['res.users'].sudo().browse(userid)
        token = user_obj.token
        url = ""
        headers = {
            'Authorization': 'Bearer' + str(token),
            'x-authorization': 'RlYVynDl9ALmOtfCotsLS9iSr93bMzgpIWfoxLktznLfTUL3NfaNO5HittoAfA9Z'}
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.content)
        designation_list = data.get('content')
        for desg in designation_list:
            self.env.cr.execute('select d.id from hr_designation as d where d.name = %s', [desg.get('DesignationName')])
            desg = self.env.cr.fetchall()
            if not desg:
                vals= {
                    'name': desg['DesignationName'],
                    'designation_id':desg['DesignationId'],
                    'designation_code':desg['DesignationCode'],
                    'create_date': desg['CreatedOn'],
                    'modified_on_date': desg['ModifiedOn'],
                    'is_active': desg['IsActive'],
                    'create_uid': desg['CreatedBy'] or False,
                }
                self.env['designation.master'].sudo().create(vals)

