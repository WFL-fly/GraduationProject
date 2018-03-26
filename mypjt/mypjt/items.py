# -*- coding: utf-8 -*-

import scrapy
class MypjtItem(scrapy.Item):
      data_list=scrapy.Field()
      top_list=scrapy.Field()
      #currentPageIndex=scrapy.Field()
      currency_name=scrapy.Field()
      new_update_date=scrapy.Field()
'''
class OtherItem(scrapy.Item):
      data_list=scrapy.Field()
      top_list=scrapy.Field()
      currency_name=scrapy.Field()
      new_update_date=scrapy.Field()
'''