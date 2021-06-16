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

esquema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "DocNum": {
                "type": "string"
                },
                "DocDate": {
                "type": "string"
                },
                "CardCode": {
                "type": "string"
                },
                "CardName": {
                "type": "string"
                },
                "WarehouseCode": {
                "type": "string"
                },
                "DatosProdOC": {
                "type": "array",
                "items": [
                    {
                    "type": "object",
                    "properties": {
                        "ItemCode": {
                        "type": "string"
                        },
                        "ItemDescription": {
                        "type": "string"
                        },
                        "Quantity": {
                        "type": "number"
                        },
                        "MeasureUnit": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "ItemCode",
                        "ItemDescription",
                        "Quantity",
                        "MeasureUnit"
                    ]
                    },
                    {
                    "type": "object",
                    "properties": {
                        "ItemCode": {
                        "type": "string"
                        },
                        "ItemDescription": {
                        "type": "string"
                        },
                        "Quantity": {
                        "type": "number"
                        },
                        "MeasureUnit": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "ItemCode",
                        "ItemDescription",
                        "Quantity",
                        "MeasureUnit"
                    ]
                    },
                    {
                    "type": "object",
                    "properties": {
                        "ItemCode": {
                        "type": "string"
                        },
                        "ItemDescription": {
                        "type": "string"
                        },
                        "Quantity": {
                        "type": "number"
                        },
                        "MeasureUnit": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "ItemCode",
                        "ItemDescription",
                        "Quantity",
                        "MeasureUnit"
                    ]
                    }
                ]
                }
            },
            "required": [
                "DocNum",
                "DocDate",
                "CardCode",
                "CardName",
                "WarehouseCode",
                "DatosProdOC"
            ]
            }


class helpdesk_webservice(http.Controller):

    @http.route(['/api/wsaddticket',], auth="public", type="json", method=['POST'], csrf=False)
    def wsaddticket(self, **post):
        post = yaml.load(request.httprequest.data)
        res = {}
        hd_token = uuid.uuid4().hex
        mensaje_error = {			
                        "Token": hd_token,
                        "RespCode":-1,
                        "RespMessage":"Error de conexión"
                    }
        mensaje_correcto = {		
                    "Token": hd_token,
                    "RespCode":0,				
                    "RespMessage":"OC recibidas correctamente"				
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
                uid = user_id
                nuevo_ticket = {
                    'kanban_state': 'normal',
                    'name': 'ticket prueba'
                }

                ticket_nuevo = request.env['helpdesk.ticket'].sudo().create(nuevo_ticket)
                return mensaje_correcto

        except Exception as e:
            return {			
                    "Token": token,		
                    "RespCode":-1,		
                    "RespMessage":"Error de conexión",
                    "error": e.args
                }

