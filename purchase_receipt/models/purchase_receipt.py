# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class account_voucher_line(osv.osv):
    _inherit = 'account.voucher.line'

    _columns = {
    	'taxes_id': fields.many2many('account.tax', 'voucher_line_taxe_rel', 'voucher_line_id', 'tax_id', 'Taxes'),
    }


