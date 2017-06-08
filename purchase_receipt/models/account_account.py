# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class AccountAcount(osv.osv):
    _inherit = 'account.account'

    _columns = {
        'filter_type': fields.char('Filter Type', related="user_type.code"),
    }

    # def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
    #     if not args:
    #         args = []
    #     args = args[:]
    #     ids = []
    #     if name:
    #         ids = self.search(cr, uid, [('filter_type', operator, name + "%")] ,
    #                           limit=limit)
    #     else:
    #         ids = self.search(cr, uid, args, limit=limit)
    #         # if not ids:
    #         #     ids = self.search(cr, uid,
    #         #                   [('name', operator, name)] + args,
    #         #                       limit=limit)
    #     return self.name_get(cr, uid, ids, context=context)