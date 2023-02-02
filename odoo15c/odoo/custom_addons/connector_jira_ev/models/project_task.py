# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = 'project.task'


    task_id_jira = fields.Char(string="Issue ID(Jira)")
    task_key_jira = fields.Char(string="Issue Key(Jira)")
    priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent'),('highest','Highest'),('high','High'),('medium','Medium'),('low','Low'),('lowest','Lowest')])


