# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError



class ClientMaster(models.Model):
    _name = 'client.master'
    _description = 'Client Master'

    # _inherit = [
    #     'mail.thread',
    #     'mail.activity.mixin'
    # ]


    name = fields.Char(string="Name")
    account_id = fields.Integer(string="Account ID")
    account_name = fields.Char(string="Account Name")
    account_code = fields.Char(string="Account Code")
    modified_on_date = fields.Datetime(string="Modified On")
    mail = fields.Char(string="Email")
    password = fields.Char(string="Password")
    user_check_tick = fields.Boolean(default=False, compute="user_checking")
    user_id = fields.Many2one('res.users',string="User")
    # account_type = fields.Selection([('')])


    def create_user(self):
        if not self.mail:
            raise UserError(
                _('Please set Mail for the client.'))
        if not self.password:
            raise UserError(
                _('Please set password for the client.'))
        user_id = self.env['res.users'].create({'name': self.name, 'login': self.mail, 'password': self.password})
        self.user_check_tick = True
        self.user_id = user_id.id
        self.mail = user_id.login


    @api.depends('user_id')
    def user_checking(self):
        if self.user_id:
            self.user_check_tick = True
        else:
            self.user_check_tick = False



    def get_clients(self):
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
        clients_list = data.get('content')
        self.env.cr.execute('select c.id from client_master as c where c.account_code = %s', (data['AccountName']))
        client = self.env.cr.fetchall()
        if not client:
            vals= {
                'account_name': data['AccountName'],
                'account_code': data['AccountName'],
                'account_id':data['AccountId'],
                'create_date': data['CreatedOn'],
                'modified_on_date': data['ModifiedOn'],
                'create_uid': data['CreatedBy'] or False,
            }
            self.env['client.master'].sudo().create(vals)