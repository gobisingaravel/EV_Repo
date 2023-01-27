# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.osv import expression



class AvailableAccessories(models.Model):
    _name = 'available.accessories'
    _description = 'Available Accessories'

    name = fields.Char(string="Name")