# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class account_voucher_line(osv.osv):
    _inherit = 'account.voucher.line'

    _columns = {
    	'taxes_id': fields.many2many('account.tax', 'voucher_line_taxe_rel', 'voucher_line_id', 'tax_id', 'Taxes'),
    }

class account_voucher(osv.osv):
    _inherit = 'account.voucher'

    def onchange_price(self, cr, uid, ids, line_ids, tax_id, partner_id=False, context=None):
        res = super(account_voucher, self).onchange_price(cr, uid, ids, line_ids, tax_id, partner_id, context)
        compute_line = self.compute_vals_for_onchange_price(cr, uid, ids, line_ids, partner_id)
        res['value']['tax_amount'] = res['value']['tax_amount'] + compute_line
        res['value']['amount'] = res['value']['amount'] + compute_line
        return res

    def compute_vals_for_onchange_price(self, cr, uid, ids, line_ids, partner_id, context=None):
        line_ids = self.resolve_2many_commands(cr, uid, 'line_ids', line_ids, ['amount','taxes_id'], context)

        tax_pool = self.pool.get('account.tax')
        partner_pool = self.pool.get('res.partner')
        position_pool = self.pool.get('account.fiscal.position')
        voucher_line_pool = self.pool.get('account.voucher.line')
        voucher_pool = self.pool.get('account.voucher')
        tax_plus = 0.0
        partner = partner_pool.browse(cr, uid, partner_id) or False
        for line in line_ids:
            if line.get('amount',False) and line.get('taxes_id', False):
                if line.get('taxes_id', []) != []:
                    taxes =  line.get('taxes_id')
                    tax_ids = []
                    if isinstance(taxes[0], tuple):
                        if taxes[0][0] == 6:
                            tax_ids = taxes[0][2]
                    elif isinstance(taxes[0], list):
                        tax_ids = taxes[0]
                    if context is None: context = {}
                    amount_line = line.get('amount',0.0)

                    for record in tax_ids:
                        record = tax_pool.browse(cr, uid, record, context=context)
                        taxes = position_pool.map_tax(cr, uid, partner and partner.property_account_position or False,
                                                      record, context=context)
                        taxs = tax_pool.browse(cr, uid, taxes, context=context)
                        for tax in taxs:
                            for tax_line in tax_pool.compute_all(cr, uid, tax, amount_line, 1).get(
                                    'taxes', []):
                                if tax_line != []:
                                    tax_plus += tax_line.get('amount', 0.0)
        return tax_plus

    def compute_tax(self, cr, uid, ids, context=None):
        res = super(account_voucher, self).compute_tax(cr, uid, ids, context=context)
        self.compute_tax_all_line(cr, uid, ids, context)
        return res

    def compute_tax_all_line(self, cr, uid, ids, context=None):
        tax_pool = self.pool.get('account.tax')
        partner_pool = self.pool.get('res.partner')
        position_pool = self.pool.get('account.fiscal.position')
        voucher_line_pool = self.pool.get('account.voucher.line')
        voucher_pool = self.pool.get('account.voucher')
        if context is None: context = {}

        amount_total = 0.0
        tax_total = 0.0
        plus_tax = False
        for voucher in voucher_pool.browse(cr, uid, ids, context=context):
            plus_tax = 0.0
            for line in voucher.line_ids:
                line_total = 0.0
                if line.taxes_id and len(line.taxes_id) > 0:
                    tax_line = 0.0
                    for tax in line.taxes_id:
                        partner = partner_pool.browse(cr, uid, voucher.partner_id.id, context=context) or False
                        taxes = position_pool.map_tax(cr, uid, partner and partner.property_account_position or False,
                                                      tax, context=context)
                        tax = tax_pool.browse(cr, uid, taxes, context=context)
                        for tax_line in tax_pool.compute_all(cr, uid, tax, line.untax_amount or line.amount, 1).get(
                                'taxes', []):
                            if tax_line != []:
                                plus_tax += tax_line.get('amount', 0.0)
            tax_total = voucher.tax_amount + plus_tax
            amount_total = voucher.amount + plus_tax
            if not context.get('no_write_from_onchange', False):
                self.write(cr, uid, [voucher.id], {'amount': amount_total, 'tax_amount': tax_total})
        if not plus_tax :
            plus_tax = 0.0
        return {'amount': amount_total, 'tax_amount': plus_tax}