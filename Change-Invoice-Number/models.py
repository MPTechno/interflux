from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class account_invoice(models.Model):
	_inherit = "account.invoice"

	number = fields.Char(related='move_id.name', store=True, copy=False)

	_sql_constraints = [
		('number_uniq', 'CHECK(1=1)',
			'Invoice Number must be unique per Company!'),
	]

	@api.multi
	def write(self, vals):
		invoice_ids = self.env['account.invoice'].search([])

		if vals.get('number'):
			for i in invoice_ids:
				if i.number == vals.get('number'):
					if i.company_id == self.company_id and i.journal_id == self.journal_id and i.type == self.type:
						raise Warning(_("Invoice Number must be unique per Company!"))
		return super(account_invoice, self).write(vals)