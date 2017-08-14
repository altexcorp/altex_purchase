# -*- coding: utf-8 -*-
# © 2009 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import urllib

from lxml import html


from openerp.addons.currency_rate_update import services


class AlgerianCentralBankGetter(services.CurrencyGetterInterface):

    code = 'ALGRIAN CB'
    name = 'ALGERIAN Central Bank'

    supported_currency_array = [
        "USD", "EUR", "GBP", "JPY","DZD","CNH","CHF","CAD","DKK","SEK","NOK","AED","SAR","KWD","TND","MAD"
    ]

    def get_updated_currency(
            self, currency_array,
            main_currency, max_delta_days):
        """implementation of abstract method of curreny_getter_interface"""


        url = "http://www.bank-of-algeria.dz/html/marcheint2.htm"

        # check if currency exist in available currencies
        self.validate_cur(main_currency)
        tree = html.fromstring(urllib.urlopen(url).read())

        # Get the list of currencies
        usd_currency = tree.xpath(
            '//*[@id="table1"]/tr[3]/td[2]/font/text()')
        other_currencies = tree.xpath(
            '//*[@id="table1"]/tr[3]/td[2]/p/font/text()')


        for elm in range(len(other_currencies)):
            other_currencies[elm] = other_currencies[elm].split( )[1]

        usd_currency[0]=usd_currency[0].split( )[1]

        currency_list = usd_currency + other_currencies
        exchange_rates = tree.xpath(
            '//*[@id="table1"]/tr[3]/td[3]/p/font/text()')

        currency_rates = dict(zip(currency_list, exchange_rates))

        if main_currency in currency_array:
            currency_array.remove(main_currency)
        for curr in currency_array:
            self.validate_cur(curr)
            val = float(currency_rates[curr])
            val = 1 / val
            if val:
                self.updated_currency[curr] = val
            else:
                raise Exception('Could not update the %s' % curr)
        return self.updated_currency, self.log_info
