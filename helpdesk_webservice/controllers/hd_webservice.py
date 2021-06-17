# -*- coding: utf-8 -*-
from odoo.tools.translate import _
from odoo import http
from odoo import http
from odoo.http import request
from datetime import datetime
from bs4 import BeautifulSoup
import json
import sys
import uuid
from odoo import http
from odoo.http import request, Response
import jsonschema
from jsonschema import validate
import json
import yaml
from . import as_estructuras
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta, datetime, date
import calendar
from dateutil.relativedelta import relativedelta
import os.path
from werkzeug import urls
from werkzeug.wsgi import wrap_file


class helpdesk_webservice(http.Controller):

    @http.route(['/api/wsaddticket', ], auth="public", type="json", method=['POST'], csrf=False)
    def wsaddticket(self, **post):
        post = yaml.load(request.httprequest.data)
        res = {}
        hd_token = uuid.uuid4().hex
        mensaje_error = {			
                        "Token": hd_token,
                        "RespCode": -1,
                        "RespMessage": "Error de conexión"
                    }
        mensaje_correcto = {
                    "Token": hd_token,
                    "RespCode": 0,
                    "RespMessage": "OC recibidas correctamente"
            }
        try:
            myapikey = request.httprequest.headers.get("Authorization")
            if not myapikey:
                return mensaje_error
            user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
            request.uid = user_id
            if user_id:
                res['token'] = hd_token
                post = post['params']
                _logger.info("\n\nvamos aqui: %s", hd_token)
                rut = post['params']['rut']
                email = post['params']['email']
                asunto = post['params']['asunto']
                kanban_state = "normal"
                descripcion = post['params']['description']
                _logger.info("\n\n\n\ndescripcion: %s", descripcion)
                uid = user_id
                nuevo_ticket = {
                    'kanban_state': kanban_state,
                    'name': asunto,
                    'description': descripcion,
                    'email': email
                }

                ticket_nuevo = request.env['helpdesk.ticket'].sudo().create(nuevo_ticket)
                return mensaje_correcto

        except Exception as e:
            return {
                    "Token": hd_token,
                    "RespCode": -1,
                    "RespMessage": "Error de conexión",
                    "error": e.args
                }
