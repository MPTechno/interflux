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
            if discount > 0:
                res[line.id] = res[line.id] - (res[line.id] * discount/100)
        return res

    _columns = {
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
        'discount': fields.float('Discount'),
    }
#
# class PurchaseOrder(models.Model):
#     _inherit = "purchase.order"
#
#     @api.depends('order_line.price_subtotal','discount_val','discount_meth','discount_type')
#     def _amount_all(self):
#         for order in self:
#             amount_untaxed = amount_tax = amount_discount = 0.0
#             for line in order.order_line:
#                 amount_untaxed  += line.price_subtotal
#                 # FORWARDPORT UP TO 10.0
#                 if order.company_id.tax_calculation_rounding_method == 'round_globally':
#                     taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
#                     amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
#                 else:
#                     amount_tax += line.price_tax
#             if order.discount_val and order.discount_meth == 'fixed' and order.discount_type:
#                 amount_discount += order.discount_val
#             elif order.discount_val and amount_untaxed and order.discount_meth == 'percentage':
#                 if order.discount_type == 'before':
#                     amount_discount += amount_untaxed * order.discount_val / 100
#                 elif order.discount_type == 'after':
#                     amount_discount += (amount_untaxed  + amount_tax) * order.discount_val / 100
#                 else:
#                     amount_discount = 0
#             order.update({
#                 'amount_untaxed': order.currency_id.round(amount_untaxed),
#                 'amount_tax'    : order.currency_id.round(amount_tax),
#                 'amount_total'  : amount_untaxed + amount_tax - amount_discount,
#                 'discount_total': amount_discount
#             })
#     discount_type  = fields.Selection([('before','Before Tax'),('after','After Tax')], string='Discount Type')
#     discount_meth  = fields.Selection([('fixed','Fixed'),('percentage','Percentage')], string='Discount Method')
#     discount_val   = fields.Float(string='Discount Value')
#     discount_total = fields.Float('Discounted Amount', compute='_amount_all')
#     amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
#     amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
#     amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')