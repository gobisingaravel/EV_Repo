# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models



class CountryMaster(models.Model):
    _name = 'country.master'
    _description = 'Country Master'

    name = fields.Char(string="Name")