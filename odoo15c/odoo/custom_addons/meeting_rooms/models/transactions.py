# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.tools import format_datetime, is_html_empty
from odoo.exceptions import UserError





class Transactions(models.Model):
    _name = 'meeting.transactions'
    _description = 'Transactions'


    name = fields.Char(string="Name")
    country_id = fields.Many2one('res.country',string="Country")
    country_master_id = fields.Many2one('country.master', string="Country")
    office_id = fields.Many2one('meeting.office',string="Office",domain="[('country_master_id', '=', country_master_id)]")
    start_date = fields.Datetime(
        'Start Date', store=True, tracking=True)
    stop_date = fields.Datetime(
        'End Date', store=True, tracking=True)
    meeting_room_id = fields.Many2one('meeting.rooms',string="Meeting Room",domain="[('country_master_id', '=', country_master_id),('office_id', '=', office_id)]")
    status = fields.Selection(
        [('booked', 'Booked'), ('notbooked', 'Not Booked')],
        string='Status',default='notbooked')
    meetings_id = fields.Many2one('meetings.details',string="Meeting ID")
    user_id = fields.Many2one('res.users',default=lambda self: self.env.uid)

    meeting_room_ids = fields.Many2many('meeting.rooms', 'transactions_room_rel', 'transactions_id', 'meeting_room_id',
                                      'Meeting Rooms')



    def configure_meeting(self):
        meeting = self.env['meetings.details']
        for rec in self:
            meetings_id = meeting.search([('meeting_room_id','=',rec.meeting_room_id.id),('country_master_id','=',rec.country_master_id.id),('office_id','=',rec.office_id.id),('start_date','>=',rec.start_date),('stop_date','<=',rec.stop_date)],limit=1)
            if meetings_id:
                raise UserError(
                    _('You may not be able to book this meeting room while it is currently booked by %s for other meeting.',meetings_id.user_id.name))
            else:
                vals = {'name': rec.name,
                        'country_master_id':rec.country_master_id.id,
                        'office_id':rec.office_id.id,
                        'user_id': rec.user_id.id,
                        'meeting_room_id':rec.meeting_room_id.id,
                        'start_date':rec.start_date,
                        'stop_date':rec.stop_date}

                meeting_id = meeting.create(vals)
                rec.meetings_id = meeting_id.id
                rec.status = 'booked'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }


    def unlink(self):
        if self.meetings_id:
            self.meetings_id.unlink()
        return super(Transactions, self).unlink()





