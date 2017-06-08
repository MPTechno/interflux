from openerp import models, api, _
from openerp.exceptions import Warning
from openerp import api, fields, models, tools


class AccountVoucherLine(models.Model):

	_inherit = 'account.voucher.line'


	@api.multi
	def _compute_partner_id(self):
		asset_type = self.env['ir.model.data'].get_object_reference('account', 'data_account_type_asset')[1]
		asset_view_type = self.env['ir.model.data'].get_object_reference('account', 'account_type_asset_view1')[1]
		liability_type = self.env['ir.model.data'].get_object_reference('account', 'data_account_type_liability')[1]
		liability_view_type = self.env['ir.model.data'].get_object_reference('account', 'account_type_liability_view1')[1]

		bank_type = self.env['ir.model.data'].get_object_reference('account', 'data_account_type_bank')[1]
		cash_type = self.env['ir.model.data'].get_object_reference('account', 'data_account_type_cash')[1]
		expense_type = self.env['ir.model.data'].get_object_reference('account', 'data_account_type_expense')[1]
		equity_type = self.env['ir.model.data'].get_object_reference('l10n_vn', 'account_type_cash_equity')[1]

		account_ids = self.env['account.account'].search([('user_type', 'in', [asset_type, asset_view_type, liability_type, liability_view_type,
																			   bank_type, cash_type, expense_type, equity_type ])])
		return [('id', 'in', account_ids.ids)]

	account_id = fields.Many2one('account.account', 'Account', required=True, domain=_compute_partner_id)