# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.osv import expression



class MeetingRooms(models.Model):
    _name = 'meeting.rooms'
    _description = 'Meeting Rooms'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]


    name = fields.Char(string="Name")
    country_id = fields.Many2one('res.country',string="Country")
    country_master_id = fields.Many2one('country.master', string="Country")
    state_id = fields.Many2one('res.country.state',string="State")
    capacity = fields.Integer(string="Capacity")
    state = fields.Selection(
        [('available', 'Available'), ('unavailable', 'Unavailable')],
        string='Status', group_expand='_group_expand_states',
        default='available', required=True, tracking=True,
        help='Shows the availability of a meeting room')
    is_available = fields.Boolean(compute='_compute_is_available', search='_search_is_available')
    office_id = fields.Many2one('meeting.office',string="Office",domain="[('country_master_id', '=', country_master_id)]")
    transactions_id = fields.Many2one('meeting.transactions',string="Transactions")
    available_access_ids = fields.Many2many('available.accessories',string="Available")




    @api.depends('state')
    def _compute_is_available(self):
        for room in self:
            room.is_available = room.state == 'available'


    def _search_is_available(self, operator, operand):
        negative = operator in expression.NEGATIVE_TERM_OPERATORS
        if (negative and operand) or not operand:
            return [('state', '=', 'unavailable')]
        return [('state', '=', 'available')]


    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

