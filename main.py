#coding:utf-8
'''
读取hst文件
'''

import struct
import time       
import datetime
import hstutils
import json
import threading
import initEnvironment 
#import tushare as ts
#import pandas as pd 
import traceback
import requests as rq
import akshare as ak
import Ashare  as ash
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S',
#                    filename='log/iceblaze.log',
#                    filemode='w')
# 配置控制台打印
# 设置控制台日志打印格式
#formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
#console = logging.StreamHandler()
#console.setFormatter(formatter)
#console.setLevel(logging.DEBUG)
#logging.getLogger('').addHandler(console)



hst_file_path ="../history/default/"
filepath = ""


start_date1 = "20000101"
end_date1= time.strftime("%Y%m%d",time.gmtime())
#end_date1 = "20220101"

"""
获取历史数据
"""
def getHistory(symbol,period,point):
    plist = []
    if symbol == ""  or symbol is None:
        print( "wrongful  symbol")
        return plist
    try:
        # 日线数据从akshare获取
        if period == 1440:
            period = "daily"
            if 'zs' in symbol:
            # print "get_k_data",symbol,period
                data = ak.index_zh_a_hist(symbol=symbol.replace('zs', ''), period="daily", start_date=start_date1, end_date=end_date1)

           

            # print "get_k_data",symbol,period
            else:
                data = ak.stock_zh_a_hist(symbol, period,start_date=start_date1, end_date=end_date1, adjust="")
            # print "=========",symbol,":",period
            if data is None:
                print("akshare is no data symbol %s period %s",symbol,period,)
                return plist
            resultlist = []
            lens = len(data)
            for unit in data.iterrows():
                dates = unit[1]['日期']
        #             长度等于10的是%Y-%m-%d格式,16的是%Y-%m-%d %H:%M 格式
                dataformate = "%Y-%m-%d %H:%M"
                date_len = len(dates)
                if date_len == 10 :
                    dataformate = "%Y-%m-%d"
                d=datetime.datetime.strptime(dates,dataformate)
                times=int(time.mktime(d.timetuple()))
                opens=unit[1]['开盘']
                close=unit[1]['收盘']
                high=unit[1]['最高']
                low=unit[1]['最低']
                volume=unit[1]['成交量']
                
                times = int(times)
                opens = hstutils.floatHandle(opens,point)
                high = hstutils.floatHandle(high,point)
                low = hstutils.floatHandle(low,point)
                close = hstutils.floatHandle(close,point)
                volume = int(volume)
                
                priceStruc = hstutils.PriceStruct(times, opens, high, low, close,volume)
                plist.append(priceStruc)
            return plist
        else:
           
            
            # 分钟数据从ashare获取
            period = "60m"
            if 'sh' or 'sz' in symbol:
            # print "get_k_data",symbol,period
                data = ash.get_price(symbol, frequency=period,count=3600)

            # print "=========",symbol,":",period
            if data is None:
                print("ashare is no data symbol %s period %s",symbol,period,)
                return plist
            resultlist = []
            lens = len(data)
            for unit in data.iterrows():
                dates = unit[1]['day']
        #             长度等于10的是%Y-%m-%d格式,16的是%Y-%m-%d %H:%M 格式
                dataformate = "%Y-%m-%d %H:%M:%S"
                #date_len = len(dates)
                d=datetime.datetime.strptime(dates,dataformate)
                times=int(time.mktime(d.timetuple()))
                opens=unit[1]['open']
                close=unit[1]['close']
                high=unit[1]['high']
                low=unit[1]['low']
                volume=unit[1]['volume']
                
                times = int(times)
                opens = hstutils.floatHandle(opens,point)
                high = hstutils.floatHandle(high,point)
                low = hstutils.floatHandle(low,point)
                close = hstutils.floatHandle(close,point)
                volume = int(volume)
                
                priceStruc = hstutils.PriceStruct(times, opens, high, low, close,volume)
                plist.append(priceStruc)
            return plist
    except Exception as e:
        return []
    



"""
开始运行某个周期的图表
"""


def startChartRun(symbol,period):
    symbol_names = symbol
    filename = hst_file_path+symbol_names+str(period)+".hst"
    point = 2;
    # 写入头部

    hstutils.writeHstHead(filename,symbol_names,period,point)
    # 写入一个时间段的历史数据
    plist = getHistory(symbol,period,point)
    if plist is not None:
        hstutils.writeStructList(filename,plist);

    
"""
启动一个图表数据的实时线程
"""


def startThread():
    while symbolList:
        code = symbolList.pop()
        periodList = [5,15,30,60,1440]
        for period in periodList:
            t = threading.Thread(target=startChartRun,args=(code,period))
            t.start()
if __name__ == '__main__':
    print("environment init start ....................................")
#     初始化raw文件,并返回所有股票代码
    symbolList = initEnvironment.initFunc()

    threads = []
# 启动线程数量100
    for i in range(100):
        t = threading.Thread(target=startThread)
        
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("over .........................close window and open MT4")
print("please press enter")
input()