# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_sale_cancel(self, cr, uid, ids, context=None):
        picking_obj = self.pool.get('stock.picking')
        picking_type_obj = self.pool.get('stock.picking.type')
        self.write(cr, uid, ids, {
            'state': 'cancel'
        }, context=context)
        for order in self.browse(cr, uid, ids, context=context):
            for picking in order.picking_ids:
                picking_type_ids = picking_type_obj.search(cr, uid, [('name', '=', 'Receipts')], limit=1)
                for picking_type_id in picking_type_ids:
                    new_picking = picking_obj.copy(cr, uid, picking.id, default={
                        'picking_type_id': picking_type_id,
                        'state': 'confirmed',
                    }, context=context)
            order_id = self.copy(cr, uid, order.id, context=context)
            ## TODO: Create incomming shipment

            return {
                'name': _("Sale Order"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'sale.order',
                'res_id': order_id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'domain': '[]',
                'context': context
            }
        return True
        # result = self.action_cancel(cr, uid, ids, context=context)
        # if result:
        #     self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        # return result