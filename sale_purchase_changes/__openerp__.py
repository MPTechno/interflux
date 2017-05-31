# -*- coding: utf-8 -*-

{
    'name': 'Sale/Purchase Changes',
    'version': '1.0',
    'summary': 'Sale/Purchase Changes',
    'description': """
        Sale/Purchase Changes
    """,
    'author': 'HashMicro / Bharat Chauhan',
    'website': 'www.hashmicro.com',
    'category': 'Sale / Purchase',
    'depends': ['sale', 'purchase', 'stock'],
    'data': [
        'views/purchase_view.xml',
        'views/sale_view.xml',
        'views/stock_inventory_view.xml',
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
