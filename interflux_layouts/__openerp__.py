# -*- coding: utf-8 -*-
{
    'name': "interflux_layouts",

    'summary': """
        - Edit printouts's format
        - Create Tab Product & P/N for Customer
        - Create new printout
        """,

    'description': """
        1. Create Tab Product & P/N for Customer
        2. Edit Delivery Address field to Text type.
        3. Edit format of Sale/Quotation, Purchase Order and Delivery Order Printouts
        4. Create a Invoice Printouts
        5. Create a Request Purchase Quotation Printouts
    """,

    'author': "HashMicro / Hoang",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'HashMicro',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product',
        'sale',
        'account',
        'purchase_discount',
        'sale_account_invoice_discount',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_layout.xml',
        'report/report_purchase_order.xml',
        'report/report_picking.xml',
        'report/report_sale_order.xml',
        'report/report_quotation_sale_order.xml',
        'report/report_invoice.xml',
        'report/report_supplier_invoice.xml',
        'report/report_customer_invoice.xml',
        'report/report_purchase_quotation.xml',
        'interflux_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
