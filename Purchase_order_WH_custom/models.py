from openerp import models, fields, api
from openerp.osv import orm


class PurchaseOrderLine(orm.Model):
    _inherit = 'purchase.order.line'

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        'Source Warehouse',
        help="If a source warehouse is selected,"
	     "it will be used to define the route.")


