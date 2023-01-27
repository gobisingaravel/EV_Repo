# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class MeetingBookedWizard(models.TransientModel):
    _name = "meeting.booked.wizard"
    _description = "Message wizard to display success messages"

    def get_default(self):
        if self.env.context.get("message", False):
            return self.env.context.get("message")
        return False

    name = fields.Text(string="Message", readonly=True, default=get_default)
