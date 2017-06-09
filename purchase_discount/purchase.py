# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class PurchaseOrderLine(osv.osv):
	_inherit = "purchase.order.line"

	def _calc_line_base_price(self, cr, uid, line, context=None):
		"""Return the base price of the line to be used for tax calculation.

		This function can be extended by other modules to modify this base
		price (adding a discount, for example).
		"""
		return line.price_unit

	def _calc_line_quantity(self, cr, uid, line, context=None):
		"""Return the base quantity of the line to be used for the subtotal.

		This function can be extended by other modules to modify this base
		quantity (adding for example offers 3x2 and so on).
		"""
		return line.product_qty

	def _amount_line(self, cr, uid, ids, prop, arg, context=None):
		res = {}
		cur_obj=self.pool.get('res.currency')
		tax_obj = self.pool.get('account.tax')
		for line in self.browse(cr, uid, ids, context=context):
			line_price = self._calc_line_base_price(cr, uid, line, context=context)
			line_qty = self._calc_line_quantity(cr, uid, line, context=context)
			discount = line.discount
			taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line_price, line_qty, line.product_id, line.order_id.partner_id)
			cur = line.order_id.pricelist_id.currency_id
			res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
			# if discount > 0:
			# 	res[line.id] = res[line.id] - (res[line.id] * discount/100)
		return res

	_columns = {
		'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
		'discount': fields.float('Discount'),
	}

class PurchaseOrder(osv.osv):
	_inherit = "purchase.order"

	def _amount_line_tax(self, cr, uid, line, context=None):
		val = 0.0
		line_obj = self.pool['purchase.order.line']
		price = line.price_unit
		if line.discount_method == 'fix':
			price = price - line.discount
		elif line.discount_method == 'per':
			price = price - (line.price_unit * ((line.discount or 0.0) / 100.0))
		else:
			price = price
		qty = line.product_qty or 0.0
		for c in self.pool['account.tax'].compute_all(
				cr, uid, line.taxes_id, price, qty, line.product_id,
				line.order_id.partner_id)['taxes']:
			val += c.get('amount', 0.0)
		return val

	def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		order_discount = 0.0
		cur_obj=self.pool.get('res.currency')
		line_obj = self.pool['purchase.order.line']
		for order in self.browse(cr, uid, ids, context=context):
			res[order.id] = {
				'amount_untaxed': 0.0,
				'amount_tax': 0.0,
				'amount_total': 0.0,
			}
			val = val1 = 0.0
			cur = order.pricelist_id.currency_id
			order_discount = order.discount_amt
			for line in order.order_line:
				val1 += line.price_subtotal
				val += self._amount_line_tax(cr, uid, line, context=context)
			res[order.id]['amount_tax']=cur_obj.round(cr, uid, cur, val)
			res[order.id]['amount_untaxed']=cur_obj.round(cr, uid, cur, val1)
			res[order.id]['amount_total']=res[order.id]['amount_untaxed'] + res[order.id]['amount_tax'] - order_discount
		return res

	def _get_order(self, cr, uid, ids, context=None):
		result = {}
		for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
			result[line.order_id.id] = True
		return result.keys()

	def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
		res = super(PurchaseOrder, self)._prepare_inv_line(cr, uid, account_id=account_id, order_line=order_line, context=context)
		res.update({'discount_method': order_line.discount_method,
					'discount_amount': order_line.discount,
					})
		return res

	_columns = {
		'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
			store={
				'purchase.order.line': (_get_order, None, 10),
			}, multi="sums", help="The amount without tax", track_visibility='always'),
		'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Taxes',
			store={
				'purchase.order.line': (_get_order, None, 10),
			}, multi="sums", help="The tax amount"),
		'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
			store={
				'purchase.order.line': (_get_order, None, 10),
			}, multi="sums", help="The total amount"),
		}