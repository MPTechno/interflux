from openerp import _, api, exceptions, fields, models
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError

class stock_invoice_onshipping(models.TransientModel):
    _inherit = "stock.invoice.onshipping"
    
    #Override for move discount from purchase to invoice. 
    def open_invoice(self):
        context = self.env.context
        if context is None:
            context = {}
        pick_ids = context.get('active_ids')
        journal2type = {'sale':'out_invoice', 'purchase':'in_invoice' , 'sale_refund':'out_refund', 'purchase_refund':'in_refund'}
        inv_type = journal2type.get(self.journal_type) or 'out_invoice'
        pick_info = self.env['stock.picking'].browse(pick_ids)
        lst_partner = [x.partner_id.id for x in pick_info]
        lst_partner = list(set(lst_partner))
        if len(lst_partner) > 1:
            raise UserError('The partner must be same!')
        invoice_ids = False
        for pickid in pick_info:
            if pickid.state != 'done':
                raise UserError('Do not allow users to proceed if Delivery Order status is not Done')
            purchase_id = pickid.purchase_id
            # prepare invoice
            date_invoice = self.invoice_date
            partner_id = purchase_id.partner_id.id
            journal_id = self.journal_id.id
            currency_id = purchase_id.currency_id.id
            account_id = purchase_id.partner_id.property_account_payable_id.id
            total_aditional_discount = 0
            for invoice_id in purchase_id.invoice_ids:
                total_aditional_discount += float(invoice_id.discount_total or 0.00)
            if not invoice_ids:
                invoice_ids = self.env['account.invoice'].create({
                'date_invoice': date_invoice and date_invoice or False,
                'partner_id'  : partner_id,
                'journal_id'  : journal_id,
                'currency_id' : currency_id,
                'account_id'  : account_id,
                'doc_source'  : '%s,%s' %('stock.picking',pickid.id),
                'type'        : inv_type,
                'discount_total':str(float(purchase_id.discount_total or 0.00) - total_aditional_discount),
            })
            self.env.cr.execute(''' Insert into invoice_picking_rel values(%s,%s) '''%(str(invoice_ids.id),str(pickid.id)))
            line = [{'pol_id': i.purchase_line_id, 'qty': i.product_uom_qty} for i in pickid.move_lines if i.purchase_line_id]
            #purchase_id.order_line
            # prepare invoice line
            if line:
                for l in line:
                        invl = self._prepare_invoice_line_from_po_line(l)
                        invl.update({'invoice_id': invoice_ids.id})
                        self.env['account.invoice.line'].create(invl)
            if not invoice_ids:
                raise UserError('No invoice created!')
            for stkm in pickid.move_lines:
                stkm.write({'invoice_state': 'invoiced'})
        return {
                'name': 'Invoice',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'views': [(self.env.ref('account.invoice_supplier_form').id, 'form')],
                'type': 'ir.actions.act_window',
                'res_id': invoice_ids.id,
                'target': 'current'
            }
    
