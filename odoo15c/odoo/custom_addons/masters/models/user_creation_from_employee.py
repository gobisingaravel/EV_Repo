# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import json


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    user_check_tick = fields.Boolean(default=False,compute="user_checking")
    password = fields.Char(string="Password")
    date_hired = fields.Date(string="Date Hired")
    termination_date = fields.Date(string="Termination Date")
    employee_num = fields.Char(string="Employee Number")
    bhr_num = fields.Char(string="Bhr Num")
    emp_fname = fields.Char(string='First Name', copy=True)
    emp_mname = fields.Char(string='Middle Name', copy=True)
    emp_lname = fields.Char(string='Last Name', copy=True)
    nick_name = fields.Char(string="Nick Name")
    employment_status_id = fields.Many2one('status.master',string="Employment Status")
    designation_id = fields.Many2one('designation.master',string="Designation")
    user_response_id = fields.Char(string="ID")
    token = fields.Char(string="Token")
    dpa_ticket_at = fields.Datetime(string="DPA Ticket")


    def get_data(self):
        data = {}
        user_id = self.env.user
        uid = user_id.user_res_id
        url = "https://evox2.eastvantage.com/api/user/%s/my_team_list"%uid
        # payload = {'username': user_id.login,
        #            'password': user_id.password}
        payload = {}
        headers = {
            'Authorization': 'Bearer' + str(user_id.token),
            'x-authorization': 'RlYVynDl9ALmOtfCotsLS9iSr93bMzgpIWfoxLktznLfTUL3NfaNO5HittoAfA9Z'}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.content)

        # vals= {
        #     'name': data['name'],
        #     'employee_num':data['emp_num'],
        #     'date_hired': data['date_hired'],
        #     'designation_id': data['designation_id'],
        #     'emp_fname': data['emp_fname'],
        #     'emp_lname': data['emp_lname']
        # }
        # self.env['hr.employee'].sudo().create(vals)


    @api.onchange('emp_fname', 'emp_mname', 'emp_lname')
    def get_employee_name(self):
        for emp_name in self:
            fname = self.emp_fname if self.emp_fname else ''
            mname = self.emp_mname if self.emp_mname else ''
            lname = self.emp_lname if self.emp_lname else ''
            emp_name.name = (str(fname) + ' ' + str(mname) + ' ' + str(lname)).title()



    def create_user(self):
        user_id = self.env['res.users'].create({'name': self.name,'login': self.work_email,'password': self.password})
        self.address_home_id = user_id.partner_id.id
        self.user_check_tick = True
        self.user_id = user_id.id
        self.work_email = user_id.login


    @api.depends('address_home_id','user_id')
    def user_checking(self):
        if self.user_id:
            self.user_check_tick = True
        else:
            self.user_check_tick = False

