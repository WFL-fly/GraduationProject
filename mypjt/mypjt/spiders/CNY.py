
# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import logging
from scrapy.selector import Selector
from scrapy.http import Request
from mypjt.items  import MypjtItem
import time,datetime
import traceback
from  mypjt.Public_Module import check_all_currency_tb,currency_translate_dict
logger=logging.getLogger(sys._getframe().f_code.co_filename)#os.path.abspath('.')+
def getGroupData(List_item):
    temp_res=[]
    res3=Selector(text=List_item[0]).xpath('//td/text()').extract()
    temp_res.append(currency_translate_dict[res3[0]])#name
    for i in List_item[1:6]:
        res3=Selector(text=i).xpath('//td/text()').extract()
        if len(res3)>0:
           res4=res3[0]#货币名称
        else :
           res4="0.00"
        temp_res.append(float(res4))
    res3=Selector(text=List_item[-2]).xpath('//td/text()').extract()#date
    datetime=res3[0]+' '
    res3=Selector(text=List_item[-1]).xpath('//td/text()').extract()#time
    datetime +=res3[0]#datetime str
    temp_res.append(datetime)
    return temp_res

class CnySpider(scrapy.Spider):
    name = 'CNY'
    allowed_domains = ['www.boc.cn']
    start_urls = ['http://www.boc.cn/sourcedb/whpj/']

    def __init__(self):
        super(CnySpider,self).__init__()
        self.datetime=None
        self.currentPageIndex=0
        self.allPagesNum=None
        self.item=MypjtItem()
        self.item['data_list']=[]
        self.item['currency_name']='CNY'
        logger.info('init  %s log' % self.name)
        logFilePath=os.path.join(os.path.abspath('.'),'logfile')
        if  not os.path.exists(logFilePath):
            logger.info ("directory %s no exists， create new directory" % logFilePath)
            os.mkdir(logFilePath)
        logFilePath=os.path.join(logFilePath,'{0}.log'.format(self.name))
        logger.info('init log sucessful')
        #获取最新的更新时间
        self.datetime=check_all_currency_tb('CNY',"CNY_tb")
        self.item['new_update_date']=self.datetime
    def parse(self, response):
        logger.info('提取数据')        
        #提取总页数
        #global allPagesNum
        if  self.allPagesNum==None:
            res=response.xpath('/html/body/div[@class="wrapper"]/div[@class="BOC_main"]/div[@class="pb_ft clearfix"]/div[@class="turn_page"]/p/span/text()').extract()
            if len(res)>0 :
                if  res[0].isdigit():
                    self.allPagesNum=int(res[0])
                    logger.info("获取总页数成功"+res[0])
                else:
                    self.allPagesNum=0
                    logger.error("提取数据文本错误")
            else:
                self.allPagesNum=0
                logger.error("未获取到总页数")
       
        #得到table
        res=response.xpath('//table[@align="left"]//tr').extract()#可以使用
        #得到表头
        self.item['top_list']=Selector(text=res[0]).xpath('//th/text()').extract()
        #得到货币汇率数据
        page_data=[]
        for index in range(1,len(res)):
            res2=Selector(text=res[index]).xpath('//td').extract()
            group_Res=getGroupData(res2)
            page_data.append(group_Res)
        self.currentPageIndex+=1
        page_datetime=datetime.datetime.strptime(page_data[0][-1],'%Y-%m-%d %H:%M:%S')
        #print(page_datetime)
        if  self.datetime==None:
            logger.error('get CNY update time error')
            return 
        else:
            if  page_datetime <=self.datetime or self.currentPageIndex>=self.allPagesNum :
                if  len(self.item['data_list'])>0:
                    yield self.item
                    logger.info("get all pages data")
                    return
                else:
                    logger.info("cannot get valid data")
                    return
        if  page_datetime>self.item['new_update_date']:
            self.item['new_update_date']=page_datetime
        self.item['data_list'].append(page_data)
        #print(datetimestr)
        
        #item['currentPageIndex']=self.currentPageIndex
        logger.info(self.currentPageIndex)
       
        #爬取后面的网页数据
        if  self.currentPageIndex<self.allPagesNum:
            new_url='http://www.boc.cn/sourcedb/whpj/index_{0}.html'.format(self.currentPageIndex)
            logger.info(new_url)
            yield Request(new_url,callback=self.parse)
        

