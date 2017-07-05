# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta
import openerp
from openerp import tools
from openerp import SUPERUSER_ID
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning
from openerp.osv import osv


class mrp_production(models.Model):
    _inherit = "mrp.production"

    @api.model
    def _default_name_sequence(self):
        order_type = self._context.get('type', 'man')
        if order_type=='man':
            name = self.env['ir.sequence'].next_by_code('mrp.production')
        else:
            name = self.env['ir.sequence'].next_by_code('assembly.assembly') 
        return name

    name = fields.Char(string='Name', required=True, states={'draft': [('readonly', False)]}, copy=False,
        default=_default_name_sequence)
    mrp_remark = fields.Text('Remark')

    type = fields.Selection([
            ('man','Manufacturing'),
            ('assembly','Assembly'),
        ], string='Type', default=lambda self: self._context.get('type', 'man'),
        track_visibility='always')