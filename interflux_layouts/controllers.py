# -*- coding: utf-8 -*-
from openerp import http

# class InterfluxLayouts(http.Controller):
#     @http.route('/interflux_layouts/interflux_layouts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/interflux_layouts/interflux_layouts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('interflux_layouts.listing', {
#             'root': '/interflux_layouts/interflux_layouts',
#             'objects': http.request.env['interflux_layouts.interflux_layouts'].search([]),
#         })

#     @http.route('/interflux_layouts/interflux_layouts/objects/<model("interflux_layouts.interflux_layouts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('interflux_layouts.object', {
#             'object': obj
#         })