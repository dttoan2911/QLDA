# -*- coding: utf-8 -*-
from odoo import http

# class Scrum(http.Controller):
#     @http.route('/scrum/scrum/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scrum/scrum/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('scrum.listing', {
#             'root': '/scrum/scrum',
#             'objects': http.request.env['scrum.scrum'].search([]),
#         })

#     @http.route('/scrum/scrum/objects/<model("scrum.scrum"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scrum.object', {
#             'object': obj
#         })