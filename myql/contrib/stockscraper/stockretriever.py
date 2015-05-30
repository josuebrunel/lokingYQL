"""This module isn't mine, it's at 99% inspired from https://github.com/gurch101/StockScraper written by Gurchet Rai.
So all rigts reserved to Gurchet Rai.
Documentation http://www.gurchet-rai.net/dev/yahoo-finance-yql
"""

from __future__ import absolute_import

import datetime
from datetime import date, timedelta

from myql.myql import MYQL

class StockRetriever(MYQL):

    def __init__(self, format='json', debug=False, oauth=None):
        """Initialize the object
        """
        super(StockRetriever, self).__init__(community=True, format=format, debug=debug, oauth=oauth)


    def get_current_info(self, symbolList, columns=None, format='json'):
        """get_current_info() uses the yahoo.finance.quotes datatable to get all of the stock information presented in the main table on a typical stock page 
        and a bunch of data from the key statistics page.
        """
        response = self.select('yahoo.finance.quotes',columns).where(['symbol','in',symbolList])
        return response

    def get_news_feed(self, symbol,format='json'):
        """get_news_feed() uses the rss data table to get rss feeds under the Headlines and Financial Blogs headings on a typical stock page.
        """
        rss_url='http://finance.yahoo.com/rss/headline?s={0}'.format(symbol)
        response = self.select('rss',['title','link','description'],limit=2).where(['url','=',rss_url])
        return response

    def get_historical_info(self, symbol,items=None, startDate=None, endDate=None, limit=None, format='json'):
        """get_historical_info() uses the csv datatable to retrieve all available historical data on a typical historical prices page
        """
        today = date.today()
        start_date = datetime.date(day=today.day - 7,month=today.month - 1, year=today.year)
        end_date = datetime.date(day=today.day - 1,month=today.month - 1, year=today.year)

        startDate = startDate if startDate else str(start_date)
        endDate = endDate if endDate else str(end_date)

        response = self.select('yahoo.finance.historicaldata',items,limit).where(['symbol','=',symbol],['startDate','=',startDate],['endDate','=',endDate])
        return response

    def get_options_info(self, symbol, items=[], expiration='', format=format):
        """get_options_data() uses the yahoo.finance.options table to retrieve call and put options from the options page.
        """
        response = self.select('yahoo.finance.options',items).where(['symbol','=',symbol],[] if not expiration else ['expiration','=',expiration])
        return response

    def get_index_summary(self, symbol, items=[],format='json'):
        """
        """
        response = self.select('yahoo.finance.quoteslist',items).where(['symbol','=',symbol])
        return response

    def get_industry_index(self, index_id,items=[],format='json'):
        """retrieves all symbols that belong to an industry.
        """
        response = self.select('yahoo.finance.industry',items).where(['id','=',index_id])
        return response
