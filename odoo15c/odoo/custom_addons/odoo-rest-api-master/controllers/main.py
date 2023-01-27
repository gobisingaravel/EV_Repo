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
            if rec['name']:
                vals = {
                    'name': rec['name'],
                    'work_email': rec['work_email']
                }
                new_user = request.env['hr.employee'].sudo().create(vals)
                new_user.create_user()
                args = {'message':'Success','Id':new_user.id,'success':True}
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
                    'name': rec['name']
                }
                new_country = request.env['country.master'].sudo().create(vals)
                args = {'message': 'Success', 'Id': new_country.id, 'success': True}
        return args


    @http.route('/create_department', type='json', auth='none')
    def create_department(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
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









