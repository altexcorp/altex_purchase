# coding: utf-8

from openerp import models , fields , api, _
import openerp.addons.decimal_precision as dp
import dateutil.parser
from openerp.tools import french_number
import re

class Altex_purchases(models.Model):
	_name    = 'purchase.order'
	_inherit = 'purchase.order'

	date_order_bc = fields.Date(string="date order bc", compute="_computedate")

	def _computedate(self):
		self.date_order_bc = dateutil.parser.parse(self.date_order).date()

	def amount_to_text_fr(self, amount, currency='DZD'):
		number = '%.2f' % amount
		units_name = currency
		list = str(number).split('.')
		start_word = french_number(abs(int(list[0])))
		end_word = french_number(int(list[1]))
		cents_number = int(list[1])
		cents_name = (cents_number > 1) and ' Centimes' or ' Centime'

		expression = "un Mille"
		if re.search(expression, start_word) is not None:
			start_word = re.sub(r'un Mille', 'Mille', start_word)

		expression = "un Cent"
		if re.search(expression, start_word) is not None:
			start_word = re.sub(r'un Cent', 'Cent', start_word)

		final_result = start_word + ' ' + units_name + ' ' + end_word + ' ' + cents_name
		return final_result


class Purchase_Change_Date(models.Model):
	_inherit = "purchase.order.line"
	product_qty = fields.Integer(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True)
