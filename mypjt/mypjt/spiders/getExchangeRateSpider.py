# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from mypjt.items  import MypjtItem
import time,datetime
class GetexchangeratespiderSpider(scrapy.Spider):
    name = 'getExchangeRateSpider'
    allowed_domains = ['www.boc.cn']
    start_urls = ['http://www.boc.cn/sourcedb/whpj/']

    def parse(self, response):
        item=MypjtItem（）
        #res=response.xpath('//table[ @align = "left"]/text()').extract()#.encode('utf-8')
        # res=response.selector.xpath('//table[ @align = "left"]/tr[i]/td/text()').extract()
        #res=response.xpath('//table[@align="left" or @width="100%"]/tr')
        #res=response.xpath('normalize-space(//table[@align="left"]/tr)')
        res=response.xpath('//table[@align="left"]//tr').extract()#可以使用
        for index, link in enumerate(res):
            res2=Selector(text=link).xpath('//td').extract()
            if len(res2)<8 :
              break
            res3=Selector(text=res2[0]).xpath('//td/text()').extract()
            if len(res3)>0:
               item.currency_name=res3[0]#货币名称
            else :
                item.currency_name=0.00
            res3=Selector(text=res2[1]).xpath('//td/text()').extract()
            if len(res3)>0:
                item.price_of_purchasing_spot_exchange= float(res3[0])#现汇买入价
            else :
                item.price_of_purchasing_spot_exchange=0.00

            res3=Selector(text=res2[2]).xpath('//td/text()').extract()
            if len(res3)>0:
                item.price_of_purchasing_foreign_cash= float(res3[0])#现钞买入价
            else :
                item.price_of_purchasing_foreign_cash=0.00

            res3=Selector(text=res2[3]).xpath('//td/text()').extract()
            if len(res3)>0:
                item.price_of_selling_spot_exchange= float(res3[0])#现汇卖出价
            else :
                item.price_of_selling_spot_exchange=0.00
            res3=Selector(text=res2[4]).xpath('//td/text()').extract()
            if len(res3)>0:
                item.price_of_selling_foreign_cash= float(res3[0])#现钞卖出价
            else :
                item.price_of_selling_foreign_cash=0.00

            res3=Selector(text=res2[5]).xpath('//td/text()').extract()
            if len(res3)>0:
                item.translation_price= float(res3[0])#折算价
            else :
                item.translation_price=0.00

            res3=Selector(text=res2[6]).xpath('//td/text()').extract()
            if len(res3)>0:
                item.release_date=time.strptime(res3[0],"%Y-%m-%d")
            else :
                item.release_date=datetime.datetime.now().strftime("%Y-%m-%d")

            res3=Selector(text=res2[7]).xpath('//td/text()').extract()
            if len(res3)>0:
                item.release_time=time.strptime(res3[0],"%H-%M-%S")
            else :
                item.release_time=datetime.datetime.now().strftime("%H:%M:%S")
            #res4="   "
            #for ele in range(1,len(res2)):
            #    res3=Selector( text=res2[ele] ).xpath('//td/text()').extract()
             #   if len(res3):
             #       res4 += res3[0]+'   '
            #    else:
            #        res4 +='XXX'+"    "
            #print(res4)