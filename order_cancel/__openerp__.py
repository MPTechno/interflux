# -*- coding: utf-8 -*-
{
    'name': "order_cancel",

    'summary': """
        Purchase/Sale Order Cancel""",

    'description': """
        Purchase/Sale Order Cancel
    """,

    'author': "HashMicro / Hoang",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/purchase_order.xml',
        'views/sale_order.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}