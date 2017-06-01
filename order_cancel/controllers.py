# -*- coding: utf-8 -*-
from openerp import http

# class PurchaseOrderCancel(http.Controller):
#     @http.route('/purchase_order_cancel/purchase_order_cancel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_cancel/purchase_order_cancel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_cancel.listing', {
#             'root': '/purchase_order_cancel/purchase_order_cancel',
#             'objects': http.request.env['purchase_order_cancel.purchase_order_cancel'].search([]),
#         })

#     @http.route('/purchase_order_cancel/purchase_order_cancel/objects/<model("purchase_order_cancel.purchase_order_cancel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_cancel.object', {
#             'object': obj
#         })