# -*- coding: utf-8 -*-
import logging
import ctypes
import os
import sys
#from scrapy.settings  import LOG_FILE
#控制台日志颜色设置
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.
FOREGROUND_DICT={'FOREGROUND_WHITE':0x07,'FOREGROUND_BLUE':0x01,'FOREGROUND_GREEN':0x02, \
'FOREGROUND_RED':0x04,'FOREGROUND_INTENSITY':0x08,'FOREGROUND_YELLOW':0x06}
BACKGROUND_BLUE = 0x10 # dark blue.
BACKGROUND_GREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.
BACKGROUND_DICT={'BACKGROUND_WHITE':0x70,'BACKGROUND_BLUE':0x10,'BACKGROUND_GREEN':0x20, \
'BACKGROUND_RED':0x40,'BACKGROUND_INTENSITY':0x80,'BACKGROUND_YELLOW':0x60}

STD_INPUT_HANDLE= -10
STD_OUTPUT_HANDLE=-11
STD_ERROR_HANDLE= -12

def init_logFile(logFileName):
    logFilePath=os.path.join(os.path.abspath('.'),'logfile')
    if  not os.path.exists(logFilePath):
        os.mkdir(logFilePath)
    logFilePath=os.path.join(logFilePath,'{0}.log'.format(logFileName))
    return logFilePath
logFilePath=init_logFile('logfile')

std_out_handle= ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
def set_cmd_color(color,handle=std_out_handle):
    bool =ctypes.windll.kernel32.SetConsoleTextAttribute(handle,color)
    return bool
'''
def get_cmd_color():
    int =ctypes.windll.kernel32.GetConsoleTextAttribute(handle) 
    return int
default_color=get_cmd_color()
'''
def reset_color():
    set_cmd_color(FOREGROUND_GREEN)

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
