# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp import models, fields, api


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    #Used for "Invoice" report
    @api.model
    def get_batch_number(self, obj, product_id):
    	origin = obj.origin
    	stock_picking_pool = self.env['stock.picking']
    	stock_picking = stock_picking_pool.search([('name','=',obj.origin)])
    	if stock_picking:
    		for pack_operation in stock_picking.pack_operation_ids:
    			if pack_operation.product_id == product_id:
    				return pack_operation.lot_id.name
        return ''
        
    
    #Used for "Invoice" report
    @api.model
    def get_delivery_order_number(self, obj):
    	sale_order_pool = self.env['sale.order']
    	stock_picking_pool = self.env['stock.picking']

    	if obj.origin:
			sale_obj = sale_order_pool.search([('name','=',obj.origin)])
			if sale_obj:
				return sale_obj.client_order_ref
			else:
				stock_picking_obj = stock_picking_pool.search([('name','=',obj.origin)])
				if stock_picking_obj:
					picking_origin = stock_picking_obj.origin
					sale_obj = sale_order_pool.search([('name','=',picking_origin)])
					if sale_obj:
						return sale_obj.client_order_ref
        return ''

    #Used for "Invoice" report
    @api.model
    def get_delivery_address(self, obj):
    	sale_order_pool = self.env['sale.order']
    	stock_picking_pool = self.env['stock.picking']

    	if obj.origin:
			sale_obj = sale_order_pool.search([('name','=',obj.origin)])
			if sale_obj:
				print"sale_obj.deli_address",sale_obj.deli_address
				return sale_obj.deli_address
			else:
				stock_picking_obj = stock_picking_pool.search([('name','=',obj.origin)])
				if stock_picking_obj:
					picking_origin = stock_picking_obj.origin
					sale_obj = sale_order_pool.search([('name','=',picking_origin)])
					if sale_obj:
						print"sale_obj.deli_address",sale_obj.deli_address
						return sale_obj.deli_address
        return ''
        
    #Used for "Invoice" report
    @api.model
    def get_your_po_number(self, obj):
    	sale_order_pool = self.env['sale.order']
    	stock_picking_pool = self.env['stock.picking']

    	if obj.origin:
			sale_obj = sale_order_pool.search([('name','=',obj.origin)])
			if sale_obj:
				return sale_obj.your_po_no
			else:
				stock_picking_obj = stock_picking_pool.search([('name','=',obj.origin)])
				if stock_picking_obj:
					picking_origin = stock_picking_obj.origin
					sale_obj = sale_order_pool.search([('name','=',picking_origin)])
					if sale_obj:
						return sale_obj.your_po_no
        return ''

