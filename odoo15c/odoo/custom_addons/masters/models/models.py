# -*- coding: utf-8 -*-

from odoo import models, fields, api



class EmployeePublicFullName(models.Model):
    _inherit = 'hr.employee.public'

    emp_fname = fields.Char(readonly=True)
    emp_mname = fields.Char(readonly=True)
    emp_lname = fields.Char(readonly=True)



class PartnerFullName(models.Model):
    _inherit = 'res.partner'

    partner_fname = fields.Char(string='First Name', copy=True)
    partner_mname = fields.Char(string='Middle Name', copy=True)
    partner_lname = fields.Char(string='Last Name', copy=True)


    @api.onchange('partner_fname','partner_mname','partner_lname')
    def get_partner_name(self):
        for p_name in self:
            fname = self.partner_fname if self.partner_fname else ''
            mname = self.partner_mname if self.partner_mname else ''
            lname = self.partner_lname if self.partner_lname else ''
            p_name.name = (str(fname)+' '+str(mname)+' '+str(lname)).title()


class PartnerFullName(models.Model):
    _inherit = 'res.users'

    user_fname = fields.Char(string='First Name', copy=True)
    user_mname = fields.Char(string='Middle Name', copy=True)
    user_lname = fields.Char(string='Last Name', copy=True)


    @api.onchange('user_fname','user_mname','user_lname')
    def get_partner_name(self):
        for u_name in self:
            fname = self.user_fname if self.user_fname else ''
            mname = self.user_mname if self.user_mname else ''
            lname = self.user_lname if self.user_lname else ''
            u_name.name = (str(fname)+' '+str(mname)+' '+str(lname)).title()


