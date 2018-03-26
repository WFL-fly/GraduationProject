# -*- coding: utf-8 -*-
import os
import sys
import logging
import time,datetime
import pymysql

logger=logging.getLogger(sys._getframe().f_code.co_filename)#os.path.abspath('.')+

def init_logFile(logFileName):
    logFilePath=os.path.join(os.path.abspath('.'),'logfile')
    if  not os.path.exists(logFilePath):
        logger.info ("directory %s no exists， create new directory" % logFilePath)
        os.mkdir(logFilePath)
    logFilePath=os.path.join(logFilePath,'{0}.log'.format(logFileName))
    logger.info('init log file path : %s sucessful' % logFilePath)
    return logFilePath
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