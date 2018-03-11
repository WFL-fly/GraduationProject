# -*- coding: utf-8 -*-


# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class MypjtItem(scrapy.Item):
      currency_name=scrapy.Field()

      price_of_purchasing_spot_exchange=scrapy.Field()
      price_of_purchasing_foreign_cash=scrapy.Field()
      price_of_selling_spot_exchange=scrapy.Field()
      price_of_selling_foreign_cash=scrapy.Field()
      translation _price=scrapy.Field()
      release_date=scrapy.Field()
      release_time=scrapy.Field()