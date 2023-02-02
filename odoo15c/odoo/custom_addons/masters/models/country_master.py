# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models



class CountryMaster(models.Model):
    _name = 'country.master'
    _description = 'Country Master'

    name = fields.Char(string="Name")
    country_evox_id = fields.Char(string="ID")


    def get_country(self):
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
        country_list = data.get('content')
        for country in country_list:
            self.env.cr.execute('select c.id from country_master as c where c.name = %s', [country.get('name')])
            ctry = self.env.cr.fetchall()
            if not ctry:
                vals = {
                    'name': country.get('name'),
                }
                self.env['country.master'].sudo().create(vals)