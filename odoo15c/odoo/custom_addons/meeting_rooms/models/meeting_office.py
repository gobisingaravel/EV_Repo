# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models



class MeetingOffice(models.Model):
    _name = 'meeting.office'
    _description = 'Meeting office'

    name = fields.Char(string="Name")
    country_id = fields.Many2one('res.country',string="Country")
    country_master_id = fields.Many2one('country.master', string="Country")
