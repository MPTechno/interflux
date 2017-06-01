# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_purchase_cancel(self, cr, uid, ids, context=None):
        result = self.action_cancel(cr, uid, ids, context=context)
        if result:
            result = self.action_cancel_draft(cr, uid, ids, context=context)
        return result