# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
import sys
import openpyxl
from openpyxl import load_workbook
from openpyxl import workbook
from openpyxl import Workbook
from openpyxl import load_workbook
from mypjt.items  import MypjtItem

def find_file(path,filename):
    for root,dirs,filesname in os.walk(path):
        for file in filesname:
            if file==filename:
                return True
    return  False
class MypjtPipeline(object):

    def __init__(self):
        print('open excel')
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
           ws=self.allData_wb.active
           ws.append(['货币名称','现汇买入价','现钞买入价','现汇卖出价','现钞卖出价','中行折算价','发布日期','发布时间'])
        self.allData_ws=self.allData_wb.active
    def process_item(self,item,spider):
        print('write excel')
        for line in item['list_item']:
            self.allData_ws.append(line)
            filename=line[0]+'.xlsx'
            filepath=os.path.join(self.dataFilePath,filename)
            res=find_file(self.dataFilePath,filename)
            if res:
               wb=load_workbook(filepath)
            else:
               wb=Workbook()
               ws=wb.active
               ws.append(['现汇买入价','现钞买入价','现汇卖出价','现钞卖出价','中行折算价','发布日期','发布时间'])
            ws=wb.active
            datalist=line[1:len(line)]
            ws.append(datalist)
            wb.save(filepath)
        
    def close_spider(self,spider):
        print('close excel')#日志
        self.allData_wb.save(self.allDataFilePath)

    