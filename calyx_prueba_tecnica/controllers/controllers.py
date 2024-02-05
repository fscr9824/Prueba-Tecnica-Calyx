# -*- coding: utf-8 -*-
import json
import logging
import odoo
import pprint
import werkzeug
from werkzeug import urls
from datetime import datetime
from odoo import http
from odoo.http import request
from http import HTTPStatus

_logger = logging.getLogger(__name__)

class controller_requets(http.Controller):
    @http.route('/check_credit', auth='public', type='http')
    def func_requets(self, **kwargs):
        response = []
        data = json.loads(request.httprequest.data)
        cr, context, env = http.request.cr, http.request.context, http.request.env


