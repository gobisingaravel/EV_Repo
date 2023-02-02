# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.tools import format_datetime, is_html_empty
from odoo.exceptions import UserError



class Meetings(models.Model):
    _name = 'meetings.details'
    _description = 'Meetings'


    name = fields.Char(string="Name")
    country_id = fields.Many2one('res.country',string="Country")
    country_master_id = fields.Many2one('country.master', string="Country")
    office_id = fields.Many2one('meeting.office',string="Office")
    start_date = fields.Datetime(
        'Start Date', store=True, tracking=True)
    stop_date = fields.Datetime(
        'End Date', store=True, tracking=True)
    meeting_room_id = fields.Many2one('meeting.rooms',string="Meeting Room")
    user_id = fields.Many2one('res.users',string="User")
    booked = fields.Boolean(string="Booked")
