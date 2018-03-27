#!/bin/bash
#python spider auto run shell
exec &>./logfile/spider-sh.log
echo "start python spider shell"

# CNY spider

starttime=`date "+%Y-%m-%d %H:%M:%S"`
start_s=`date '+%S'`
echo "start run spider CNY , start time: $starttime"
scrapy crawl CNY
stop_s=`date '+%S'`
stoptime=`date "+%Y-%m-%d %H:%M:%S"`
runtime=$[stop_s-start_s]
echo  "CNY spider run finish , stop time: ${stoptime} ,run time : ${runtime} s."

# USD spider

starttime=`date "+%Y-%m-%d %H:%M:%S"`
start_s=`date '+%S'`
echo "start run spider USD , start time: $starttime"
scrapy crawl USD
stop_s=`date '+%S'`
stoptime=`date "+%Y-%m-%d %H:%M:%S"`
runtime=$[stop_s-start_s]
echo  "USD spider run finish , stop time: ${stoptime} ,run time : ${runtime} s."


# JPY spider

starttime=`date "+%Y-%m-%d %H:%M:%S"`
start_s=`date '+%S'`
echo "start run spider JPY , start time: $starttime"
scrapy crawl JPY
stop_s=`date '+%S'`
stoptime=`date "+%Y-%m-%d %H:%M:%S"`
runtime=$[stop_s-start_s]
echo  "JPY spider run finish , stop time: ${stoptime} ,run time : ${runtime} s."

# EUR spider

starttime=`date "+%Y-%m-%d %H:%M:%S"`
start_s=`date '+%S'`
echo "start run spider EUR , start time: $starttime"
scrapy crawl EUR
stop_s=`date '+%S'`
stoptime=`date "+%Y-%m-%d %H:%M:%S"`
runtime=$[stop_s-start_s]
echo  "EUR spider run finish , stop time: ${stoptime} ,run time : ${runtime} s."

# GBP spider

starttime=`date "+%Y-%m-%d %H:%M:%S"`
start_s=`date '+%S'`
echo "start run spider GBP , start time: $starttime"
scrapy crawl GBP
stop_s=`date '+%S'`
stoptime=`date "+%Y-%m-%d %H:%M:%S"`
runtime=$[stop_s-start_s]
echo  "GBP spider run finish , stop time: ${stoptime} ,run time : ${runtime} s."

# RUB spider
starttime=`date "+%Y-%m-%d %H:%M:%S"`
start_s=`date '+%S'`
echo "start run spider RUB , start time: $starttime"
scrapy crawl RUB
stop_s=`date '+%S'`
stoptime=`date "+%Y-%m-%d %H:%M:%S"`
runtime=$[stop_s-start_s]
echo  "RUB spider run finish , stop time: ${stoptime} ,run time : ${runtime} s."

