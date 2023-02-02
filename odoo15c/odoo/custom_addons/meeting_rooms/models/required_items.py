# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.tools import format_datetime, is_html_empty
from odoo.exceptions import UserError


class Items(models.Model):
    _name = 'required.items'
    _description = 'Required Items'


    name = fields.Char(string="Name")
