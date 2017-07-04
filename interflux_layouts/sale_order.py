# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp import models, fields, api
from datetime import date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Used for "Sale Order" report
    #Check the if the Current Date is 01.07.2017 or greater that that.
    @api.model
    def check_date_sequence(self,obj):
        if date.today().year >= 2017 and date.today().month >= 7:
            return self.so_no_report(obj)
        return obj.name
        
    @api.model
    def so_no_report(self, obj):
        result = "Q"
        date_order = obj.date_order
        sp = date_order.split("-")
        for val in sp:
            if len(val) == 4:
                year = val
        result += str(year[2:]) + "-" + str(obj.name[-3:])
        return result

