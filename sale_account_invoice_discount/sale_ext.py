from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class sale_order_line(models.Model):
    _inherit = 'sale.order.line' 
    
    @api.onchange('discount_amount')
    def onchange_discount_amount(self):
        self.discount = self.discount_amount
        
    @api.onchange('discount')
    def onchange_discount(self):
        self.discount_amount = self.discount
    
    discount_amount = fields.Float('Discount Amount')
    discount        = fields.Float('Discount (%)')