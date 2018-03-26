# -*- coding: utf-8 -*-
import scrapy
import scrapy
import os
import sys
import logging
from scrapy.selector import Selector
from scrapy.http import Request
from mypjt.items  import MypjtItem,OtherItem
import time,datetime
import pymysql
from  mypjt.Public_Module import check_all_currency_tb
logger=logging.getLogger(sys._getframe().f_code.co_filename)#os.path.abspath('.')+
def getGroupData(List_item):
    temp_res=[]
    name=List_item[0].split('/')[-1]
    temp_res.append(name)
    temp_res.append(List_item[1])
    temp_res.append(List_item[2]+':00')
    return temp_res
'''
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
                            sql=" insert into all_currency_tb(currency_name,update_datetime,currency_tb_name) VALUES('{0}','{1}','{2}') ".format(currency_name,'2010-1-1 0:00:00',currency_tb_name)
                            effect_row=cursor.execute(sql)
                            conn.commit()
                            logger.info(' insert {0} record to table {1} sucessful'.format(currency_name,'all_currency_tb') )
                        except Exception as e:
                            conn.rollback()
                            logger.info(' insert {0} record to table {1} failure'.format(currency_name,'all_currency_tb') )
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
'''
class JpySpiderSpider(scrapy.Spider):
    name = 'JPY_Spider'
    allowed_domains = ['zou114.com']
    start_urls = ['http://www.zou114.com/agiotage/hl2.asp?from=JPY&to=CNY&q=1']
    def __init__(self):
        super(JpySpiderSpider,self).__init__()
        self.currency_name='JPY'
        self.currency_tb_name=self.currency_name+'_tb'
        self.item=OtherItem()
        self.item['currency_name']=self.currency_name
        self.item['data_list']=[]
        self.item['top_list']=['货币名称','汇率','更新日期']
        self.item['new_update_date']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #print(self.item['new_update_date'])
        self.exchange_currency_list=['CNY','USD','GBP','EUR','RUB']#人民币 美元 英镑 欧元 卢布
        self.index=0
        logger.info(self.start_urls[0])
        check_all_currency_tb(self.currency_name,self.currency_tb_name)
    def parse(self, response):
        logger.info('get from {0} to {1} exchange rate'.format(self.currency_name,self.exchange_currency_list[self.index] ))
        res=response.xpath('//table[@id="table1"]//tr').extract()#可以使用
        for i in range(1,len(res)):
            res2=Selector(text=res[i]).xpath('//td/text()').extract()
            if  res2[0].split('/')[-1]==self.exchange_currency_list[self.index] :   
                res2=getGroupData(res2)
                self.item['data_list'].append(res2)  
                break
        self.index+=1
        if  self.index<len(self.exchange_currency_list):
            new_url='http://www.zou114.com/agiotage/hl2.asp?from=JPY&to={0}&q=1'.format(self.exchange_currency_list[self.index])
            logger.info(new_url)
            yield Request(new_url,callback=self.parse)
        else:
            yield  self.item
            logger.info('get from {0} exchange rate finish'.format(self.currency_name))