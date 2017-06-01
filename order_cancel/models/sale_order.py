# -*- coding: utf-8 -*-

from openerp import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_sale_cancel(self, cr, uid, ids, context=None):
        result = self.action_cancel(cr, uid, ids, context=context)
        if result:
            self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return result