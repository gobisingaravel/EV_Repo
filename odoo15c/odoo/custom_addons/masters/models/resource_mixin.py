# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from dateutil.relativedelta import relativedelta


from odoo import api, fields, models


class ResourceMixin(models.AbstractModel):
    _inherit = "resource.mixin"
    _description = 'Resource Mixin'

    resource_id = fields.Many2one(
        'resource.resource', 'Resource',
        auto_join=True, index=True, ondelete='restrict', required=False)



class ResourceCalendarAttendance(models.Model):
    _inherit = "resource.calendar.attendance"

    calendar_id = fields.Many2one("resource.calendar", string="Resource's Calendar", required=False, ondelete='cascade')


class ResourceResource(models.Model):
    _inherit = "resource.resource"
    _description = "Resources"


    calendar_id = fields.Many2one(
        "resource.calendar", string='Working Time',
        default=lambda self: self.env.company.resource_calendar_id,
        required=False, domain="[('company_id', '=', company_id)]",
        help="Define the schedule of resource")
