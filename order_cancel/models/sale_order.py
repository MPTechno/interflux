# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    version = fields.Integer(default=0)

    def action_sale_cancel(self, cr, uid, ids, context=None):
        picking_obj      = self.pool.get('stock.picking')
        picking_type_obj = self.pool.get('stock.picking.type')

        for order in self.browse(cr, uid, ids, context=context):
            order_name = order.name.split('-')[0]
            for picking in order.picking_ids:
                picking_type_ids = picking_type_obj.search(cr, uid, [('name', '=', 'Receipts')], limit=1)
                if picking.state == 'done':
                    for picking_type_id in picking_type_ids:
                        ## TODO: Create incomming shipment
                        picking_obj.copy(cr, uid, picking.id, default={
                            'picking_type_id': picking_type_id,
                            'state': 'confirmed',
                        }, context=context)



                    new_version = order.version + 1
                    self.write(cr, uid, order.id, {
                        'name': order_name,
                        'state': 'cancel',
                    }, context=context)

                    order_id = self.copy(cr, uid, order.id, default={
                        'name': '%s-%s' % (order_name, str(new_version)),
                        'version': new_version,
                    }, context=context)
                    # self.write(cr, uid, order_id, {
                    #     'name': order_name,
                    #     'version': new_version
                    # }, context=context)

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
                else:
                    return {
                        self.action_cancel(cr, uid, order.id, context=context),
                        self.write(cr, uid, order.id, {
                            'name': order_name,
                            'state': 'draft',
                        }, context=context)

                    }

        return True
        # result = self.action_cancel(cr, uid, ids, context=context)
        # if result:
        #     self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        # return result

