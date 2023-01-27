# Copyright 2016-2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class JiraConnector(models.Model):
    _name = "jira.connector"
    _description = "Jira Connector"


    name = fields.Char(string="Name")
    instance = fields.Char(string="Instance")
    login_mail = fields.Char(string="Login Email")
    api_token = fields.Char(string="Api Token")

