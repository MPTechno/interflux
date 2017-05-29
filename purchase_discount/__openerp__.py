# -*- coding: utf-8 -*-
{
    "name": "Discount module in Purchase Order",
    "author": "HashMicro/Tri Nguyen",
    "version": "8.0.1.0",
    "website": "www.hashmicro.com",
    "category": "Purchase Management",
    "depends": ['purchase', 'weight_calculation'],
    "data": [
        "views/purchase_order_view.xml",
        "views/purchase_discount_view.xml",
    ],
    'description':'''
    1.	Allow users to input discount per column. 
    2.	Add Discount column after Unit of Measure
    3.	Add field “Additional Discount” after Untaxed Amount (before Taxes) for users to input any additional discounts
    4.	Total to take into account of the Additional Discount as well
     
    Key Points:
    1.	Search for existing module for odoo 10 first
    2.	If found similar can use it and create this module to modify that module
    3.	If no similar modules then create this module
    ''',
    'demo': [],
    "installable": True,
    "auto_install": False,
    "application": True,
}