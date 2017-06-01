# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp import models, fields, api


class product_product(models.Model):
    _inherit = 'product.product'

    # product_no  = fields.Char('Product Number')
    # def name_get(self, cr, uid, ids, context=None):
    #     return_val = super(product_product, self).name_get(cr, uid, ids, context=context)
    #     res = []
    #
    #     def _name_get(d):
    #         name = d.get('name', '')
    #         code = d.get('default_code', False)
    #         if code:
    #             name = '[%s] %s' % (code, name)
    #         if d.get('variants'):
    #             name = name + ' - %s' % (d['variants'],)
    #         return (d['id'], name)
    #
    #     for product in self.browse(cr, uid, ids, context=context):
    #         res.append((product.id, (product.name)))
    #     return res or return_val


product_product()

class product_template(models.Model):
    _inherit = 'product.template'

    product_no = fields.Char('Product Number')


class ShipmentTerm(models.Model):
    _name = 'shipment.term'

    name = fields.Char('Name')

class sale_order(models.Model):
    _inherit = 'sale.order'

    deli_address    = fields.Text('Delivery Address')
    shipment_term1  = fields.Many2one('shipment.term', string='Shipment Term')
    your_po_no = fields.Char('Po No.')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # shipment_term = fields.Many2one('shipment.term', string='Shipment Term')

    @api.model
    def get_pn_code(self, order_id):
        pn_obj = self.env['interflux.pn.cod']
        order_line = self.browse(order_id)
        product_id = False
        partner_id = False
        pn_name = ''
        if order_line and order_line.id:
            if order_line.product_id and order_line.product_id.id:
                product_id = order_line.product_id.id
        if order_line.order_id:
            if order_line.order_id.partner_id and order_line.order_id.partner_id.id:
                partner_id = order_line.order_id.partner_id.id
        if product_id and partner_id:
            pn_ids = pn_obj.search([('product_id', '=', product_id), ('pn_topartner', '=', partner_id)])
            if len(pn_ids) > 0:
                for pn in pn_ids:
                    pn_name = pn.name
                return pn_name
        return ''


class Deliveryline(models.Model):
    _inherit = 'stock.move'

    @api.model
    def get_pn_code_move(self, picking_id):
        pn_obj = self.env['interflux.pn.cod']
        picking_line = self.browse(picking_id)
        product_id = False
        partner_id = False
        pn_name = ''
        if picking_line and picking_line.id:
            if picking_line.product_id and picking_line.product_id.id:
                product_id = picking_line.product_id.id
        if picking_line.picking_id:
            if picking_line.picking_id.partner_id and picking_line.picking_id.partner_id.id:
                partner_id = picking_line.picking_id.partner_id.id
        if product_id and partner_id:
            pn_ids = pn_obj.search([('product_id', '=', product_id), ('pn_topartner', '=', partner_id)])
            if len(pn_ids) > 0:
                for pn in pn_ids:
                    pn_name = pn.name
                return pn_name
        return ''

class res_partner(models.Model):
    _inherit = 'res.partner'

    pn_name         = fields.One2many('interflux.pn.cod', 'pn_topartner', string='P/N Code')
    # product_id      = fields.Many2one('product.product', string='Product Name')
    # pn_code         = fields.Char('P/N Code')


class pn_code(models.Model):
    _name = 'interflux.pn.cod'

    name = fields.Char('Name')
    product_id = fields.Many2one('product.product', string='Product')
    pn_topartner = fields.Many2one('res.partner', string='P/N')

#     @api.model
#     def create(self, vals):
#         if vals.get('pn_topartner', False) and vals.get('product_id', False):
#             vals['name'] = str(vals.get('pn_topartner')) + '-' + str(vals.get('product_id'))
#         return super(pn_code, self).create(vals)
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        res = super(PurchaseOrder, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        if partner_id:
            supplier = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            res['value']['attn_tel'] = supplier.phone
            res['value']['fax'] = supplier.fax
        # if partner_id:
        #     partner_id = self.env['res.partner'].browse(partner_id)
        #     # self.attn = self.partner_id.attn
        #     res['value']['attn_tel'] = partner_id.attn_tel
        #     res['value']['fax'] = partner_id.fax
        return res

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    attn = fields.Char('Attention')
    attn_tel = fields.Char('Tel')
    fax = fields.Char('Fax')

class sale_order(osv.osv):
    _inherit = "sale.order"

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
    	res = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=context)
    	part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
    	res['value']['telno'] = part.phone
    	res['value']['faxno'] = part.fax
    	return res
    	

class StockPicking(models.Model):

    _inherit = 'stock.picking'

    def get_so_ref(self, origin):
        sale_order = self.env['sale.order'].search([('name', '=', origin)])
        if sale_order and sale_order[0].client_order_ref:
            return sale_order[0].client_order_ref

    def get_lot_number(self, product_id, pack_operation_ids):
        lot_number = ""
        for pack_operation_id in pack_operation_ids:
            if pack_operation_id.product_id.id == product_id.id:
                if pack_operation_id.lot_id.name:
                    lot_number = pack_operation_id.lot_id.name
        return lot_number

    def get_po_number(self, origin):
        sale_order = self.env['sale.order'].search([('name', '=', origin)])
        if sale_order and sale_order[0].client_order_ref:
            return sale_order[0].your_po_no
