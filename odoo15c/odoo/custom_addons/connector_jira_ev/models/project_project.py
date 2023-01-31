# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import json

from requests.auth import HTTPBasicAuth


class Project(models.Model):
    _inherit = 'project.project'


    project_id_jira = fields.Char(string="Project Id(Jira)")
    project_key_jira = fields.Char(string="Project Key(Jira)")
    reporter_user_id = fields.Many2one('res.users',string="Reporter")


    def get_projects(self):

        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        login = user.login

        jira_key = self.env['ir.config_parameter'].sudo().get_param('connector_jira_ev.jira_key', '')

        jira_login_id = self.env['ir.config_parameter'].sudo().get_param('connector_jira_ev.jira_login', '')

        project_url = "https://eastvantage.atlassian.net/rest/api/3/project/search?jql=assignee=currentuser()&startAt=0&maxResults=100"
        auth = HTTPBasicAuth(jira_login_id, jira_key)
        headers = {
            "Accept": "application/json"
        }
        response = requests.request(
            "GET",
            project_url,
            headers=headers,
            auth=auth
        )
        data = json.loads(response.content)
        if data.get('values'):
            for projects in data.get('values'):
                self.env.cr.execute('select p.id from project_project as p where p.project_id_jira = %s and p.project_key_jira = %s',
                                    (projects['id'], projects['key']))
                project = self.env.cr.fetchall()
                if not project:
                    vals = {
                        'name': projects['name'],
                        'project_id_jira': projects['id'],
                        'project_key_jira': projects['key'],
                        'user_id': user.id,
                    }
                    project_id = self.env['project.project'].sudo().create(vals)
                else:
                    project_id = self.env['project.project'].browse(project[0])

                issue_url = "https://eastvantage.atlassian.net/rest/api/2/search?jql=status=10000 AND project={}&startAt=0&maxResults=100".format(projects['id'])

                response = requests.request(
                    "GET",
                    issue_url,
                    headers=headers,
                    auth=auth
                )
                issue_data = json.loads(response.content)
                # user_mail_url = "https://eastvantage.atlassian.net/rest/api/user/email?accountId"
                # user_url = "https://eastvantage.atlassian.net/rest/api/2/users/search?query"
                # response = requests.request(
                #     "GET",
                #     user_url,
                #     headers=headers,
                #     auth=auth
                # )
                # user_data = json.loads(response.content)
                if issue_data.get('issues'):
                    for issues in issue_data.get('issues'):
                        # user = [user['emailAddress'] for user in user_data if user['accountID'] == issues['fields']['assignee']['accountId']]
                        # if user[0]:
                        #     self.env.cr.execute(
                        #         'select u.id from res_users as u where u.login = %s',(user[0]))
                        #     user_id = self.env.cr.fetchall()
                        #     user_id = self.env['res.users'].browse(user_id[0])
                        self.env.cr.execute(
                            'select t.id from project_task as t where t.task_id_jira = %s and t.task_key_jira = %s',
                            (issues['id'], issues['key']))
                        issue = self.env.cr.fetchall()
                        if not issue:
                            vals = {
                                'name': issues['key'] + " " + issues['fields']['summary'],
                                'task_id_jira': issues['id'],
                                'task_key_jira': issues['key'],
                                'project_id': project_id.id,
                                'priority':0
                            }
                            task_id = self.env['project.task'].sudo().create(vals)
                            task_id.user_ids = [(6, 0, [user.id])]



        # issue_url = "https://eastvantage.atlassian.net/rest/api/2/search?jql="
        # response = requests.request(
        #     "GET",
        #     issue_url,
        #     headers=headers,
        #     auth=auth
        # )
        # issue_data = json.loads(response.content)
        # if issue_data.get('issues'):
        #     for issues in issue_data.get('issues'):
        #         jira_project_id = issues['fields']['project']['id']
        #         jira_project_key = issues['fields']['project']['key']
        #         self.env.cr.execute(
        #             'select p.id from project_project as p where p.project_id_jira = %s and p.project_key_jira = %s',
        #             (jira_project_id, jira_project_key))
        #         project = self.env.cr.fetchall()
        #         if project:
        #             project_id = self.env['project.project'].browse(project[0])
        #         else:
        #             mmm
        #         self.env.cr.execute('select t.id from project_task as t where t.task_id_jira = %s and t.task_key_jira = %s',
        #                 (issues['id'], issues['key']))
        #         issue = self.env.cr.fetchall()
        #         if not issue:
        #             vals = {
        #                 'name': issues['key'] + " " + issues['fields']['summary'],
        #                 'task_id_jira': issues['id'],
        #                 'task_key_jira': issues['key'],
        #                 'project_id':project_id.id,
        #             }
        #             task_id = self.env['project.task'].sudo().create(vals)
        #             task_id.user_ids = [(6, 0, [user.id])]
        #
        #
        #
        #
        #
        #










