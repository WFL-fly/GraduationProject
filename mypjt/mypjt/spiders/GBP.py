
import scrapy
import sys
from scrapy.selector import Selector
from scrapy.http import Request
from mypjt.items  import MypjtItem
import time,datetime
import pymysql
from  mypjt.Public_Module import check_all_currency_tb,getGroupData
from  mypjt.logger import init_logger
mylogger=init_logger(__name__)


class  GbpSpider(scrapy.Spider):
    name = 'GBP'
    allowed_domains = ['zou114.com']
    start_urls = ['http://www.zou114.com/agiotage/hl2.asp?from=GBP&to=CNY&q=1']
    def __init__(self):
        super(GbpSpider,self).__init__()
        self.currency_name='GBP'
        self.currency_tb_name=self.currency_name+'_tb'
        self.page_data=[]
        self.item=MypjtItem()
        self.item['currency_name']=self.currency_name
        self.item['data_list']=[]
        self.item['top_list']=['货币名称','汇率','更新日期','default']
        #print(self.item['new_update_date'])
        self.exchange_currency_list=['CNY','JPY','EUR','USD','RUB']#人民币 美元 英镑 欧元 卢布
        self.index=0
        mylogger.info(self.start_urls[0])
        check_all_currency_tb(self.currency_name,self.currency_tb_name)
    def parse(self, response):
        mylogger.info('get from {0} to {1} exchange rate'.format(self.currency_name,self.exchange_currency_list[self.index] ))
        res=response.xpath('//table[@id="table1"]//tr').extract()#可以使用
        for i in range(1,len(res)):
            res2=Selector(text=res[i]).xpath('//td/text()').extract()
            if  res2[0].split('/')[-1]==self.exchange_currency_list[self.index] :   
                res2=getGroupData(res2)
                self.page_data.append(res2) 
                break
        self.index+=1
        if  self.index<len(self.exchange_currency_list):
            new_url='http://www.zou114.com/agiotage/hl2.asp?from=GBP&to={0}&q=1'.format(self.exchange_currency_list[self.index])
            mylogger.info(new_url)
            yield Request(new_url,callback=self.parse)
        else:
            self.item['data_list'].append(self.page_data)
            self.item['new_update_date']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield  self.item
            mylogger.info('get from {0} exchange rate finish'.format(self.currency_name))
