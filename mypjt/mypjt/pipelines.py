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
class MypjtPipeline(object):
    def __init__(self):
        print('open excel')
        self.wb=load_workbook("date.xlsx")#G:\\ProgramsCode\\GitHub\\GraduationProject\\ScrapyCode\\GraduationProject\\mypjt\\mypjt\\
        self.ws=self.wb.active
    def process_item(self,item,spider):
        print('write excel')
        for line in item['list_item']:
            self.ws.append(line)
        
    def close_spider(self,spider):
        print('close excel')
        self.wb.save("date.xlsx")
