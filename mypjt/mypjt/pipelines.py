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
        self.wb=load_workbook("G:\\ProgramsCode\\GitHub\\GraduationProject\\ScrapyCode\\GraduationProject\\mypjt\\mypjt\\date.xlsx")
        self.ws=self.wb.active
    def process_item(self,item,spider):
        print('write excel')
        line=[item['name'], item['price_of_purchasing_spot_exchange'], item["price_of_purchasing_foreign_cash"], item["price_of_selling_spot_exchange"], item["price_of_selling_foreign_cash"], item["translation_price"], item["release_date"], item['release_time']]
        print(line)
        self.ws.append(line)
        #print('save data')
        #ws=self.file.active
        #row_len=len(list(ws.rows))
        #ws.cell(row=row_len,column=1) =item["currency_name"]
        #ws.cell(row=row_len,column=2) =item["price_of_purchasing_spot_exchange"]
        #ws.cell(row=row_len,column=3) =item["price_of_purchasing_foreign_cash"]
        #ws.cell(row=row_len,column=4) =item["price_of_selling_spot_exchange"]
        #ws.cell(row=row_len,column=5) =item["price_of_selling_foreign_cash"]
        #ws.cell(row=row_len,column=6) =item["translation_price"]
        #ws.cell(row=row_len,column=7) =item["release_date"]
        #ws.cell(row=row_len,column=8) =item["release_time"]    
    def close_spider(self,spider):
        print('close excel')
        self.wb.save("date.xlsx")
