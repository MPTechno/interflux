# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class AccountAcount(osv.osv):
    _inherit = 'account.account'

    _columns = {
        'filter_type': fields.char('Filter Type', related="user_type.code"),
    }