# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import logging
from scrapy.selector import Selector
from scrapy.http import Request
from mypjt.items  import MypjtItem
import time,datetime
import pymysql
logger=logging.getLogger(sys._getframe().f_code.co_filename)#os.path.abspath('.')+
def getGroupData(List_item):
    temp_res=[]
    res3=Selector(text=List_item[0]).xpath('//td/text()').extract()
    temp_res.append(res3[0])#name
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
#检查 all_currency——tb是否存在某货币，不存在则插入该货，返回值为最新更新时间
def check_all_currency_tb(currency_name,currency_tb_name):
    temp_datetime=None
    try :
        conn=pymysql.connect(host='119.23.34.166',port=3306,user='pythonspider',passwd='python@fly',db='exchange_rate',charset='utf8')
    except Exception as e:
        logger.error(' mysql connect failure')
    else:
        try:
           cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            logger.error('get cursor error')
        else: 
            try :
                sql="create table if not exists {0}(currency_name VARCHAR(20) NOT NULL PRIMARY KEY, \
                update_datetime datetime NOT NULL,currency_tb_name VARCHAR(20) NOT NULL)".format('all_currency_tb')
                effect_row=cursor.execute(sql)
                conn.commit()
                logger.info(' table %s exist' % 'all_currency_tb')
            except Exception as e:
                conn.rollback()
                logger.error('create  table %s failure' % 'all_currency_tb')
            else:
                try :
                    sql="create table if not exists {0}(exchange_currency_name varchar(20) NOT NULL PRIMARY KEY ,child_tb_name varchar(20) NOT NULL)".format(currency_tb_name)
                    effect_row=cursor.execute(sql)
                    conn.commit()
                    logger.info('table {0} exist'.format(currency_tb_name) )
                    effect_row=cursor.execute("select update_datetime from all_currency_tb where currency_name='CNY' ")
                    if  effect_row<=0:
                        try :
                            sql=" insert into all_currency_tb(currency_name,update_datetime,currency_tb_name) VALUES('{0}','{1}','{2}') ".format('CNY','2010-1-1 0:00:00','CNY_tb')
                            effect_row=cursor.execute(sql)
                            conn.commit()
                            logger.info(' insert {0} record to table {1} sucessful'.format('CNY','all_currency_tb') )
                        except Exception as e:
                            conn.rollback()
                            logger.info(' insert {0} record to table {1} failure'.format('CNY','all_currency_tb') )
                        else:
                            temp_datetime=datetime.datetime.strptime('2010-1-1 0:00:00','%Y-%m-%d %H:%M:%S')      
                    else:
                        effect=cursor.fetchone()
                        temp_datetime=effect['update_datetime']
                except  Exception as e:
                        conn.rollback()
                        logger.error('create currency table %s failure' % currency_tb_name)    
            cursor.close()
        finally:
            conn.close()
    return temp_datetime
class GetexchangeratespiderSpider(scrapy.Spider):

    name = 'getExchangeRateSpider'
    allowed_domains = ['www.boc.cn']
    start_urls = ['http://www.boc.cn/sourcedb/whpj/']
    
    def __init__(self):
        self.datetime=None
        self.currentPageIndex=0
        super(GetexchangeratespiderSpider,self).__init__()
        self.allPagesNum=None
        logger.info('init  %s log' % self.name)
        logFilePath=os.path.join(os.path.abspath('.'),'logfile')
        if  not os.path.exists(logFilePath):
            logger.info ("directory %s no exists， create new directory" % logFilePath)
            os.mkdir(logFilePath)
        logFilePath=os.path.join(logFilePath,'{0}.log'.format(self.name))
        logger.info('init log sucessful')
        #获取最新的更新时间
        self.datetime=check_all_currency_tb('CNY',"CNY_tb")
        #print(self.datetime)
    def parse(self, response):
        logger.info('提取数据')
        item=MypjtItem()
        item['data_list']=[]
        item['currency_name']='CNY'
        #提取总页数
        #global allPagesNum
        if  self.allPagesNum==None:
            res=response.xpath('/html/body/div[@class="wrapper"]/div[@class="BOC_main"]/div[@class="pb_ft clearfix"]/div[@class="turn_page"]/p/span/text()').extract()
            if len(res)>0 and res[0].isdigit():
                self.allPagesNum=int(res[0])
                logger.info("获取总页数成功")
            else:
                self.allPagesNum=0
                logger.error("获取总页数失败")
        #得到网页标题
        res=response.xpath('/html/head/title/text()').extract()
        if  len(res)<=0:
            item['name']='XXXX'
        else:
            item['name']=res[0]
        #得到table
        res=response.xpath('//table[@align="left"]//tr').extract()#可以使用
        #得到表头
        item['top_list']=Selector(text=res[0]).xpath('//th/text()').extract()
        #得到货币汇率数据
        for index in range(1,len(res)):
            res2=Selector(text=res[index]).xpath('//td').extract()
            group_Res=getGroupData(res2)
            item['data_list'].append(group_Res)
        #print(item['data_list'][0])
        '''
        page_datetime=datetime.datetime.strptime(item['data_list'][0][-1],'%Y-%m-%d %H:%M:%S')
        if  self.datetime==None or page_datetime <=self.datetime :
            msg='rate no update {0} ---{1}'.format(self.datetime,page_datetime)
            self.logger.info(msg)
            return 
        '''
        #print(datetimestr)
        self.currentPageIndex+=1
        item['currentPageIndex']=self.currentPageIndex
        logger.info(self.currentPageIndex)
        yield item
        
        #爬取后面的网页数据
        if  self.currentPageIndex<self.allPagesNum:
            new_url='http://www.boc.cn/sourcedb/whpj/index_{0}.html'.format(self.currentPageIndex)
            logger.info(new_url)
            yield Request(new_url,callback=self.parse)
        
