# -*- coding: utf-8 -*-
import json
import math
import logging
import requests

from odoo import http, _, exceptions
from odoo.http import request




_logger = logging.getLogger(__name__)


def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }


class OdooAPI(http.Controller):
    @http.route(
        '/auth/',
        type='json', auth='none', methods=["POST"], csrf=False)
    def authenticate(self, *args, **post):
        try:
            login = post["login"]
        except KeyError:
            raise exceptions.AccessDenied(message='`login` is required.')

        try:
            password = post["password"]
        except KeyError:
            raise exceptions.AccessDenied(message='`password` is required.')

        try:
            db = post["db"]
        except KeyError:
            raise exceptions.AccessDenied(message='`db` is required.')

        http.request.session.authenticate(db, login, password)
        res = request.env['ir.http'].session_info()
        return res



    @http.route('/get_users',type='json', auth='none')
    def get_users(self, *args, **post):
        user_rec = request.env['res.users'].sudo().search([])
        users_list = []
        for user in user_rec:
            vals = {
                'name': user.name,
                'user_res_id':user.user_res_id,
                'id':user.id
            }
            users_list.append(vals)
        data = {
            'status':200,
            'users':users_list,
            'message':'Success'
        }
        return data


    @http.route('/create_users', type='json', auth='none')
    def create_user(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                employee_id = request.env['hr.employee'].sudo().search([('user_response_id','=',rec['id'])])
                country_id = request.env['country.master'].sudo().search([('country_evox_id','=',rec['country_id'])])
                if rec['department_id']:
                    department_id = request.env['hr.department'].sudo().search([('department_id', '=', rec['department_id'])])
                    if department_id:
                        department = department_id.id
                    else:
                        department_obj = request.env['hr.department'].sudo().create({'name':rec['department_name'],'department_id':rec['department_id']})
                        department = department_obj.id
                if rec['job_title']:
                    designation_id = request.env['designation.master'].sudo().search([('name', '=', rec['job_title'])])
                    if designation_id:
                        designation = designation_id.id
                    else:
                        designation_obj = request.env['designation.master'].sudo().create({'name':rec['job_title']})
                        designation = designation_obj.id
                if not employee_id:
                    vals = {
                        'user_response_id':rec['id'],
                        'name': rec['name'],
                        'job_title':rec['job_title'],
                        'work_email': rec['work_email'],
                        'mobile_phone': rec['mobile_phone'],
                        'password': rec['password'],
                        'employee_num': rec['employee_num'],
                        'bhr_num': rec['bhr_num'],
                        'nick_name': rec['nick_name'],
                        'birthday': rec['birthday'],
                        'date_hired': rec['date_hired'],
                        'designation_id': designation,
                        'department_id': department,
                        'country_master_id': country_id.id,
                    }
                    new_user = request.env['hr.employee'].sudo().create(vals)
                    args = {'message':'Success','Id':new_user.id,'success':True}
                    return args
                else:
                    employee_id.update({
                        'work_email': rec['work_email'],
                        'password': rec['password'],
                        'mobile_phone': rec['mobile_phone'],
                        'employee_num': rec['employee_num'],
                        'bhr_num': rec['bhr_num'],
                        'nick_name': rec['nick_name'],
                        'name': rec['name'],
                        'birthday': rec['birthday'],
                        'date_hired': rec['date_hired'],
                        'job_title': rec['job_title'],
                        'department_id': department,
                        'designation_id': designation,
                        'country_master_id': country_id.id,
                    })
                    employee_id.user_id.update({
                        'login': rec['work_email'],
                        'password': rec['password'],
                        'employee_num': rec['employee_num'],
                        'bhr_num': rec['bhr_num'],
                        'nick_name': rec['nick_name'],
                        'name': rec['name'],
                        'date_hired': rec['date_hired'],
                        'designation_id': designation,
                        'country_master_id': country_id.id,
                    })
                    # employee_id.work_email = rec['work_email']
                    # employee_id.password = rec['password']
                    # employee_id.mobile_phone = rec['mobile_phone']
                    # employee_id.employee_num = rec['employee_num']
                    # employee_id.bhr_num = rec['bhr_num']
                    # employee_id.nick_name = rec['nick_name']
                    # employee_id.name = rec['name']
                    # employee_id.birthday = rec['birthday']
                    # employee_id.date_hired = rec['date_hired']
                    # employee_id.department_id = department
                    # employee_id.designation_id = designation
                    # employee_id.job_title = rec['job_title']
                    # employee_id.user_id.login = rec['work_email']
                    # employee_id.user_id.password = rec['password']

                    args = {'message': employee_id.name +" "+'already exist, Updated the record with new info', 'success': True}
                    return args


    @http.route('/create_clients', type='json', auth='none')
    def create_clients(self, **rec):
        if request.jsonrequest:
            client_obj = request.env['client.master']
            if rec['name']:
                vals = {
                    'name': rec['name']
                }
                new_client = client_obj.sudo().create(vals)
                args = {'message': 'Success', 'Id': new_client.id, 'success': True}
        return args


    @http.route('/create_country', type='json', auth='none')
    def create_country(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name'],
                }
                new_country = request.env['country.master'].sudo().create(vals)
                args = {'message': 'Success', 'Id': new_country.id, 'success': True}
        return args


    @http.route('/create_department', type='json', auth='none')
    def create_department(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                vals = {
                    'department_id': rec['id'],
                    'name': rec['name']
                }
                new_dept = request.env['hr.department'].sudo().create(vals)
                args = {'message': 'Success', 'Id': new_dept.id, 'success': True}
        return args


    @http.route('/create_designation', type='json', auth='none')
    def create_designation(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name']
                }
                designation = request.env['designation.master'].sudo().create(vals)
                args = {'message': 'Success', 'Id': designation.id, 'success': True}
        return args


    @http.route('/create_status', type='json', auth='none')
    def create_status(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name']
                }
                status = request.env['status.master'].sudo().create(vals)
                args = {'message': 'Success', 'Id': status.id, 'success': True}
        return args


    @http.route('/create_location', type='json', auth='none')
    def create_location(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name']
                }
                location = request.env['location.master'].sudo().create(vals)
                args = {'message': 'Success', 'Id': location.id, 'success': True}
        return args


    @http.route('/create_supervisor', type='json', auth='none')
    def create_supervisor(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name']
                }
                supervisor = request.env['supervisor.master'].sudo().create(vals)
                args = {'message': 'Success', 'Id': supervisor.id, 'success': True}
        return args









