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
    approve_mail_sent = fields.Boolean(string="Approve Mail Sent")
    requirements_needed = fields.Boolean(string="Need IT Equipments")
    required_items_ids = fields.Many2many('required.items',string="Equipments")
    state = fields.Selection([('approved','Approved'),('waiting','Waiting for Approval')])


    def configure_meeting(self):
        meeting = self.env['meetings.details']
        for rec in self:
            meetings_id = meeting.search([('booked','=',True),('meeting_room_id','=',rec.meeting_room_id.id),('country_master_id','=',rec.country_master_id.id),('office_id','=',rec.office_id.id),('start_date','<=',rec.start_date),('stop_date','>=',rec.start_date)],limit=1)
            if meetings_id:
                raise UserError(
                    _('You may not be able to book this meeting room while it is currently booked by %s for other meeting.',meetings_id.user_id.name))
            else:
                start = rec.start_date
                end = rec.stop_date
                difference = end - start
                difference_in_seconds = difference.total_seconds()
                hours = difference_in_seconds / 3600.0

                if hours >= 2:
                    mail_template = self.env.ref('meeting_rooms.email_template_meeting_approve')
                    mail_template.send_mail(self.id, force_send=True)
                    rec.approve_mail_sent = True
                    rec.state = 'waiting'
                else:
                    vals = {'name': rec.name,
                            'country_master_id':rec.country_master_id.id,
                            'office_id':rec.office_id.id,
                            'user_id': rec.user_id.id,
                            'meeting_room_id':rec.meeting_room_id.id,
                            'start_date':rec.start_date,
                            'stop_date':rec.stop_date,
                            'booked':True}

                    meeting_id = meeting.create(vals)
                    rec.meetings_id = meeting_id.id
                    rec.status = 'booked'
                    if rec.requirements_needed and rec.required_items_ids:
                        rec.mail_it_team()

            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }


    def unlink(self):
        if self.meetings_id:
            self.meetings_id.unlink()
        return super(Transactions, self).unlink()


    def approve_meeting(self):
        meeting = self.env['meetings.details']
        for rec in self:
            vals = {'name': rec.name,
                    'country_master_id': rec.country_master_id.id,
                    'office_id': rec.office_id.id,
                    'user_id': rec.user_id.id,
                    'meeting_room_id': rec.meeting_room_id.id,
                    'start_date': rec.start_date,
                    'stop_date': rec.stop_date,
                    'booked': True}

            meeting_id = meeting.create(vals)
            rec.meetings_id = meeting_id.id
            rec.status = 'booked'
            rec.state = 'approved'
            if rec.requirements_needed and rec.required_items_ids:
                rec.mail_it_team()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def mail_it_team(self):
        mail_template = self.env.ref('meeting_rooms.email_template_it_equipments')
        mail_template.send_mail(self.id, force_send=True)


    def get_items(self):
        item = [item.name for rec in self if rec.required_items_ids for item in rec.required_items_ids]
        result = ',\n'.join(map(str, item))
        return result


