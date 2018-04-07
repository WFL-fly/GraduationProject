# -*- coding: utf-8 -*-
import os
import sys
#import logging
from scrapy.selector import Selector
import time,datetime
import pymysql
import logging
from  mypjt.logger import LoggerSet,init_logger,logFilePath

#from mypjt.settings  import LOG_FILE

#logfilepathname=init_logFile('logfile')
#cmdLogSet=LoggerSet(logging.INFO,'',['[%(asctime)s]-[%(filename)s]-[%(levelname)s]-[%(funcName)s]-[%(lineno)s] : %(message)s', '%Y-%m-%d %H:%M:%S'])
#ileLogSet=LoggerSet(logging.INFO,logFilePath,['[%(asctime)s]-[%(filename)s]-[%(levelname)s]-[%(funcName)s]-[%(lineno)d] : %(message)s', '%Y-%m-%d %H:%M:%S'])
logger=init_logger(__name__)#,fileLogSet,cmdLogSet

# 货币 中英文缩写对照dict
currency_translate_dict={'人民币':'CNY','阿联酋迪拉姆':'AED','澳大利亚元':'AUD', \
'巴西里亚尔':'BRL','加拿大元':'CAD','瑞士法郎':'CHF','丹麦克朗':'DKK','欧元':'EUR', \
'英镑':'GBP','港币':'HKD','印尼卢比':'IDR','印度卢比':'INR','日元':'JPY', \
'韩国元':'KRW','澳门元':'MOP','林吉特':'MYR','挪威克朗':'NOK','新西兰元':'NZD', \
'菲律宾比索':'PHP','卢布':'RUB','沙特里亚尔':'SAR','瑞典克朗':'SEK','新加坡元':'SGD', \
'泰国铢':'THB','土耳其里拉':'TRY','新台币':'TWD','美元':'USD','南非兰特':'ZAR' \
}
top_dict={'货币名称':'CurrencyName','现汇买入价':'BuyingRate','现钞买入价':'CashBuyingRate', \
'现汇卖出价':'SellingRate','现汇卖出价':'CashSellingRate','中行折算价':'MiddleRate'}

def getData_1(response,currency_name):
    respp=response.xpath('//div[@style="text-align: left;padding-left:10px;"]').extract()
    resppp=Selector(text=respp[0]).xpath('//b[@style="font-weight:bold;font-size:36px;font-family:Arial;"]/font[3]/text()').extract()
    ex_rate=float(resppp[0])

    list_str=respp[0].split('<br>')
    pos_1=list_str[-1].find(u'：')
    pos_2=list_str[-1].find(u'<')
    str=list_str[-1][pos_1+1:pos_2]
    str=str[:10]+' '+str[11:19]
    return [currency_name,ex_rate,str]
def getData_2(response,currency_name):
    res=response.xpath('//table[@id="table1"]//tr').extract()#可以使用
    for i in range(1,len(res)):
        res2=Selector(text=res[i]).xpath('//td/text()').extract()
        if  res2[0].split('/')[-1]==currency_name :   
            res2=getGroupData(res2)
            return res2 
def getGroupData(List_item):
    temp_res=[]
    name=List_item[0].split('/')[-1]
    temp_res.append(name)
    temp_res.append(List_item[1])
    temp_res.append(List_item[2]+':00')
    return temp_res

def init_mysql(my_host,my_port,my_user,pw,dn_name,my_charset):
        logger.info('init mysql connect')
        try :
            conn=pymysql.connect(host=my_host,port=my_port,user=my_user,passwd=pw,db=dn_name,charset=my_charset)
        except Exception as e:
            logger.error('init mysql connect failure,\n error massge: {1}'.format(childtb_name,traceback.format_exc()) )
            conn=None
        return conn

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
                    effect_row=cursor.execute("select update_datetime from all_currency_tb where currency_name='{0}' ".format(currency_name))
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