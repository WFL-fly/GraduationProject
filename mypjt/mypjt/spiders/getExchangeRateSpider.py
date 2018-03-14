# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from mypjt.items  import MypjtItem
import time,datetime
def getGroupData(List_item):
    temp_res=[]
    for i in List_item:
        res3=Selector(text=i).xpath('//td/text()').extract()
        if len(res3)>0:
           res4=res3[0]#货币名称
        else :
           res4="0.00"
        temp_res.append(res4)
    return temp_res
class GetexchangeratespiderSpider(scrapy.Spider):
    name = 'getExchangeRateSpider'
    allowed_domains = ['www.boc.cn']
    start_urls = ['http://www.boc.cn/sourcedb/whpj/']

    def parse(self, response):
        print('提取数据')
        item=MypjtItem()
        item['data_list']=[]
        #得到网页标题
        res=response.xpath('/html/head/title/text()').extract()
        if len(res)<=0:
           item['name']='XXXX'
        else:
           item['name']=res[0]
        #得到table
        res=response.xpath('//table[@align="left"]//tr').extract()#可以使用
        #得到表头
        item['top_list']=Selector(text=res[0]).xpath('//th/text()').extract()
        print(item['top_list'])
        #得到货币汇率数据
        for index in range(1,len(res)):
            res2=Selector(text=res[index]).xpath('//td').extract()
            group_Res=getGroupData(res2)
            item['data_list'].append(group_Res)
        yield item


'''
def parse(self, response):
        item=MypjtItem()
        item['list_item']=[]
        res=response.xpath('//table[@align="left"]//tr').extract()#可以使用
        for index in range(1,len(res)):
            res2=Selector(text=res[index]).xpath('//td').extract()
            #print(len(res2))
            if len(res2)<8 :
              break
            
            res3=Selector(text=res2[0]).xpath('//td/text()').extract()
            if len(res3)>0:
               item['name']=res3[0]#货币名称
            else :
               item['name']="xxx"

            res3=Selector(text=res2[1]).xpath('//td/text()').extract()
            if len(res3)>0:
                item['price_of_purchasing_spot_exchange']= float(res3[0])#现汇买入价
            else :
                item['price_of_purchasing_spot_exchange']=0.00

            res3=Selector(text=res2[2]).xpath('//td/text()').extract()
            if len(res3)>0:
                item['price_of_purchasing_foreign_cash']= float(res3[0])#现钞买入价
            else :
                item['price_of_purchasing_foreign_cash']=0.00

            res3=Selector(text=res2[3]).xpath('//td/text()').extract()
            if len(res3)>0:
                item['price_of_selling_spot_exchange']= float(res3[0])#现汇卖出价
            else :
                item['price_of_selling_spot_exchange']=0.00
            res3=Selector(text=res2[4]).xpath('//td/text()').extract()
            if len(res3)>0:
                item['price_of_selling_foreign_cash']= float(res3[0])#现钞卖出价
            else :
                item['price_of_selling_foreign_cash']=0.00

            res3=Selector(text=res2[5]).xpath('//td/text()').extract()
            if len(res3)>0:
                item['translation_price']= float(res3[0])#折算价
            else :
                item['translation_price']=0.00

            res3=Selector(text=res2[6]).xpath('//td/text()').extract()
            if len(res3)>0:
                item['release_date']=res3[0]
            else :
                item['release_date']="xxxx-xx-xx"

            res3=Selector(text=res2[7]).xpath('//td/text()').extract()
            if len(res3)>0:
                item['release_time']=res3[0]
            else :
                item['release_time']="xx-xx-xx"
        
        yield item
'''
           