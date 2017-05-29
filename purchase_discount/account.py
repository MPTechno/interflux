# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.tools import float_is_zero, float_compare
from odoo.exceptions import Warning

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"    
    pdiscount = fields.Float('Discount')
    
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity','pdiscount',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = 0
        discount_total = 0
        if self.invoice_id.type != 'in_invoice':
            price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        else:
            price = self.price_unit
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        if self.invoice_id.type == 'in_invoice':
            if self.pdiscount:
                discount_total += self.pdiscount*self.price_subtotal/100
        self.price_subtotal -= discount_total
        price_subtotal_signed -= discount_total
        if self.invoice_id.currency_id and self.invoice_id.company_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id.date_invoice).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'discount_type', 'discount_meth', 'discount_val')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(line.amount for line in self.tax_line_ids)
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        discount_total = 0
        if self.discount_val and self.discount_meth == 'fixed' and self.discount_type:
                discount_total += self.discount_val
        elif self.discount_val and self.discount_meth == 'percentage':
            if self.discount_type == 'before':
                discount_total += self.amount_untaxed * self.discount_val / 100
            elif self.discount_type == 'after':
                discount_total += (self.amount_untaxed  + self.amount_tax) * self.discount_val / 100
            else:
                discount_total = 0
        self.amount_total = self.amount_untaxed + self.amount_tax - discount_total
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign - discount_total
        self.amount_total_signed = self.amount_total * sign - discount_total
        self.amount_untaxed_signed = amount_untaxed_signed * sign - discount_total
        self.discount_total = discount_total
        
    @api.one
    @api.depends(
        'state', 'currency_id', 'invoice_line_ids.price_subtotal',
        'move_id.line_ids.amount_residual',
        'move_id.line_ids.currency_id')
    def _compute_residual(self):
        residual = 0.0
        residual_company_signed = 0.0
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        for line in self.sudo().move_id.line_ids:
            if line.account_id.internal_type in ('receivable', 'payable'):
                residual_company_signed += line.amount_residual
                if line.currency_id == self.currency_id:
                    residual += line.amount_residual_currency if line.currency_id else line.amount_residual
                else:
                    from_currency = (line.currency_id and line.currency_id.with_context(date=line.date)) or line.company_id.currency_id.with_context(date=line.date)
                    residual += from_currency.compute(line.amount_residual, self.currency_id)
        discount_total = 0
        if self.discount_total:
            discount_total = self.discount_total
        self.residual_company_signed = abs(residual_company_signed) * sign - discount_total
        self.residual_signed = abs(residual) * sign - discount_total
        self.residual = abs(residual) - discount_total
        digits_rounding_precision = self.currency_id.rounding
        if float_is_zero(self.residual - discount_total, precision_rounding=digits_rounding_precision):
            self.reconciled = True
        else:
            self.reconciled = False
    
    discount_type  = fields.Selection([('before','Before Tax'),('after','After Tax')], string='Discount Type')
    discount_meth  = fields.Selection([('fixed','Fixed'),('percentage','Percentage')], string='Discount Method')
    discount_val   = fields.Float(string='Discount Value')
    discount_total = fields.Float('Discounted Amount', compute='_compute_amount')
    amount_untaxed = fields.Monetary(string='Untaxed Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_untaxed_signed = fields.Monetary(string='Untaxed Amount in Company Currency', currency_field='company_currency_id',
        store=True, readonly=True, compute='_compute_amount')
    amount_tax = fields.Monetary(string='Tax',
        store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Monetary(string='Total',
        store=True, readonly=True, compute='_compute_amount')
    amount_total_signed = fields.Monetary(string='Total in Invoice Currency', currency_field='currency_id',
        store=True, readonly=True, compute='_compute_amount',
        help="Total amount in the currency of the invoice, negative for credit notes.")
    amount_total_company_signed = fields.Monetary(string='Total in Company Currency', currency_field='company_currency_id',
        store=True, readonly=True, compute='_compute_amount',
        help="Total amount in the currency of the company, negative for credit notes.")
    
    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        for line in self.invoice_line_ids:
            price_unit = 0
            if line.invoice_id.type != 'in_invoice':
                price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            else:
                price_unit = line.price_unit * (1 - (line.pdiscount or 0.0) / 100.0)
            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
        return tax_grouped