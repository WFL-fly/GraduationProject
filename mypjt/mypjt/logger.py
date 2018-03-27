# -*- coding: utf-8 -*-
import logging
import os
import sys

def init_logFile(logFileName):
    logFilePath=os.path.join(os.path.abspath('.'),'logfile')
    if  not os.path.exists(logFilePath):
        os.mkdir(logFilePath)
    logFilePath=os.path.join(logFilePath,'{0}.log'.format(logFileName))
    return logFilePath
logFilePath=init_logFile('logfile')
class LoggerSet(object):
    def __init__(self,Level,FilePath,Fmt_list):
        super(LoggerSet,self).__init__()
        self.level=Level
        self.file_path=FilePath
        self.fmt=logging.Formatter(Fmt_list[0],Fmt_list[1])

cmdLogSet_default=LoggerSet(logging.INFO,'',['[%(asctime)s]-[%(name)s]-[%(filename)s]-[%(levelname)s]-[%(funcName)s]-[%(lineno)d] : %(message)s', '%Y-%m-%d %H:%M:%S'])
fileLogSet_default=LoggerSet(logging.INFO,logFilePath,['[%(asctime)s]-[%(name)s]-[%(filename)s]-[%(levelname)s]-[%(funcName)s]-[%(lineno)d] : %(message)s', '%Y-%m-%d %H:%M:%S'])
def init_logger(moudle_NameAndPath='xxx',FLoggerSet=fileLogSet_default,CLoggerSet=cmdLogSet_default):
    logger = logging.getLogger(moudle_NameAndPath)
    logger.setLevel(level=logging.DEBUG)#日志等级
    #设置CMD日志
    #consoleHandler=logging.StreamHandler()
    #consoleHandler.setFormatter(CLoggerSet.fmt)
    #consoleHandler.setLevel(CLoggerSet.level)
    #logger.addHandler(consoleHandler)
    #设置文件日志
    fileHandler=logging.FileHandler(FLoggerSet.file_path)
    fileHandler.setFormatter(FLoggerSet.fmt)
    fileHandler.setLevel(FLoggerSet.level)
    logger.addHandler(fileHandler)
    return logger
