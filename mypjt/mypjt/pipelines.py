# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import logging
import os
import sys
import openpyxl
from openpyxl import load_workbook
from openpyxl import workbook
from openpyxl import Workbook
from openpyxl import load_workbook
from mypjt.items  import MypjtItem
logger=logging.getLogger('MypjtPipeline.py')
#判断sheet是否存在表头，如果不存在就创建
def sheet_is_exsit_top(ws,top_list):
    if len(tuple(ws.columns))<=0:
        ws.append(top_list)
#在工作表中查找sheet,如果没找到就创建他 create_index<0,添加到末尾
def find_wb_sheet(wb,sheet_name,create_index):
    sheet_name_list=wb.get_sheet_names()
    #sheet_name_list=wb.get_sheet_names
    res=compareListEle(sheet_name_list,sheet_name)
    if not res:
       if create_index<0:
          ws = wb.create_sheet(sheet_name)
       elif create_index>0:
          ws = wb.create_sheet(sheet_name, create_index)
       else:
          ws = wb.active
          ws.title=sheet_name
    else:
        #ws=wb.get_sheet_by_name(sheet_name)
        ws=wb[sheet_name]
    return ws    

def compareListEle(list,item):
    if len(list)<=0:
        return False
    for ele in list:
        if ele==item:
           return True
    return False
def find_file(path,filename):
    for root,dirs,filesname in os.walk(path):
        for file in filesname:
            if file==filename:
                return True
    return  False
class MypjtPipeline(object):
    
    def __init__(self):
        self.Data_wb=None
        self.excelFilePath=None
        '''
        self.allData_ws=None
        #判断数据保存文件夹是否存在，不存在则创建新文件夹
        current_abspath=os.path.abspath('.')
        self.dataFilePath=os.path.join(current_abspath,'dataFiles')
        if not os.path.exists(self.dataFilePath):
           print ("directory %s no exists， create new directory" % self.dataFilePath)
           os.mkdir(self.dataFilePath)
        self.allDataFilePath=os.path.join(self.dataFilePath,"allData.xlsx")
        res=find_file(self.dataFilePath,"allData.xlsx")
        if res:
           self.allData_wb=load_workbook(self.allDataFilePath)
        else:
           self.allData_wb=Workbook()
        '''
    def init_excel_table(self,excel_name):
        logger.info('init excel')
        current_abspath=os.path.abspath('.')
        dataFilePath=os.path.join(current_abspath,'dataFiles')
        if not os.path.exists(dataFilePath):
           print ("directory %s no exists， create new directory" % dataFilePath)
           os.mkdir(dataFilePath)
        self.excelFilePath=os.path.join(dataFilePath,excel_name+".xlsx")
        res=find_file(dataFilePath,excel_name+".xlsx")
        if res:
           self.Data_wb=load_workbook(self.excelFilePath)
        else:
           self.Data_wb=Workbook()
           #self.Data_wb.remove_sheet(self.Data_wb.get_sheet_by_name('Sheet1'))
    def process_item(self,item,spider):
        self.init_excel_table(item['name'])
        logger.info('write excel')
        top_list2=item['top_list'][1:len(item['top_list'])]
        logger.info("find sheet 0")
        allData_ws=find_wb_sheet(self.Data_wb,'allData_sheet',0)
        sheet_is_exsit_top(allData_ws,item['top_list'])
        for line in item['data_list']:
            #向总数据sheet中添加数据
            allData_ws.append(line)
            
            ws=find_wb_sheet(self.Data_wb,line[0],-1)
            sheet_is_exsit_top(ws,top_list2)
            ws.append(line[1:len(line)])
            '''
            filename=line[0]+'.xlsx'
            filepath=os.path.join(self.dataFilePath,filename)
            res=find_file(self.dataFilePath,filename)
            if res:
               wb=load_workbook(filepath)
            else:
               wb=Workbook()
               ws=wb.active
               ws.append(top_list2)
            ws=wb.active
            datalist=line[1:len(line)]
            ws.append(datalist)
            wb.save(filepath)
            '''
    def close_spider(self,spider):
        logger.info('close excel')#日志
        if self.Data_wb!=None:
           self.Data_wb.save(self.excelFilePath)
        else:
           logger.error('save excel fuail,self.Data_wb is None ')

    