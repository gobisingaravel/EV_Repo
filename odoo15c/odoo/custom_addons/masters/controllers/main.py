
import base64
import copy
import datetime
import functools
import hashlib
import io
import itertools
import json
import logging
import operator
import os
import re
import sys
import tempfile
import unicodedata
from collections import OrderedDict, defaultdict

import babel.messages.pofile
import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from lxml import etree, html
from markupsafe import Markup
from werkzeug.urls import url_encode, url_decode, iri_to_uri

import odoo
import odoo.modules.registry
from odoo.api import call_kw
from odoo.addons.base.models.ir_qweb import render as qweb_render
from odoo.modules import get_resource_path, module
from odoo.tools import html_escape, pycompat, ustr, apply_inheritance_specs, lazy_property, osutil
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools.translate import _
from odoo.tools.misc import str2bool, xlsxwriter, file_open, file_path
from odoo.tools.safe_eval import safe_eval, time
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception as _serialize_exception
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.models import check_method_name
from odoo.service import db, security
import requests
import json
from odoo.http import request, Response, JsonRequest


_logger = logging.getLogger(__name__)

CONTENT_MAXAGE = http.STATIC_CACHE_LONG  # menus, translations, static qweb

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'

COMMENT_PATTERN = r'Modified by [\s\w\-.]+ from [\s\w\-.]+'

import odoo.addons.web.controllers.main as main

import datetime
import pytz

# Shared parameters for all login/signup flows
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang'}

class Home(main.Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        main.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            evox_response = self.evox_authentication(request)
            if evox_response.get('message') == 'Successfully Login!':
                try:
                    uid = request.session.authenticate(request.session.db, request.params['login'],
                                                       request.params['password'])
                    user_id = request.env['res.users'].browse(uid)
                    user_id.token = evox_response.get('content')['access_token']
                    user_id.user_res_id = evox_response.get('content')['user']['id']

                    request.params['login_success'] = True
                    return request.redirect(self._login_redirect(uid, redirect=redirect))
                except odoo.exceptions.AccessDenied as e:
                    request.uid = old_uid
                    if e.args == odoo.exceptions.AccessDenied().args:
                        values['error'] = _("Wrong login/password")
                    else:
                        values['error'] = e.args[0]
            else:
                values['error'] = _("Please Enter EVOX Username and Password")
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        # conf_param = request.env['ir.config_parameter'].sudo()
        # orientation = conf_param.get_param('masters.orientation')
        # image = conf_param.get_param('masters.image')
        # url = conf_param.get_param('masters.url')
        #
        # background_type = conf_param.get_param('masters.background')
        #
        # if background_type == 'color':
        #     values['bg'] = ''
        #     values['color'] = conf_param.get_param('masters.color')
        # elif background_type == 'image':
        #     exist_rec = request.env['ir.attachment'].search([('is_background', '=', True)])
        #     if exist_rec:
        #         exist_rec.unlink()
        #     attachments = request.env['ir.attachment'].create({
        #         'name': 'Background Image',
        #         'datas': image,
        #         'type': 'binary',
        #         'mimetype': 'image/png',
        #         'public': True,
        #         'is_background': True
        #     })
        #     base_url = conf_param.get_param('web.base.url')
        #     url = base_url + '/web/image?' + 'model=ir.attachment&id=' + str(attachments.id) + '&field=datas'
        #     values['bg_img'] = url or ''
        # elif background_type == 'url':
        #     pre_exist = request.env['ir.attachment'].search([('url', '=', url)])
        #     if not pre_exist:
        #         attachments = request.env['ir.attachment'].create({
        #             'name': 'Background Image URL',
        #             'url': url,
        #             'type': 'url',
        #             'public': True
        #         })
        #     else:
        #         attachments = pre_exist
        #     encode = hashlib.md5(pycompat.to_text(attachments.url).encode("utf-8")).hexdigest()[0:7]
        #     encode_url = "/web/image/{}-{}".format(attachments.id, encode)
        #     values['bg_img'] = encode_url or ''
        #
        # if orientation == 'right':
        #     response = request.render('masters.login_template_right', values)
        # elif orientation == 'left':
        #     response = request.render('masters.login_template_left', values)
        # elif orientation == 'middle':
        #     response = request.render('masters.login_template_middle', values)
        # else:
        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response



    def evox_authentication(self,request):

        url = "https://evox2.eastvantage.com/server/api/auth/login"

        headers = {'Content-Type': 'application/json; charset=UTF-8',
                    'x-authorization': 'RlYVynDl9ALmOtfCotsLS9iSr93bMzgpIWfoxLktznLfTUL3NfaNO5HittoAfA9Z'}

        response = requests.request("POST", url, headers=headers, json={"username":  request.params['login'],"password":request.params['password']})
        data = json.loads(response.content)
        return data


