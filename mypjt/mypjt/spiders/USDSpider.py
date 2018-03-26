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

class UsdspiderSpider(scrapy.Spider):
    name = 'USDSpider'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
