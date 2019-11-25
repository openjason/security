#！/bin/python
'''
#sample: http://market.finance.sina.com.cn/transHis.php?symbol=sz300059&date=2019-08-26&page=2
你的问题：日线数据sina也有，但都是不复权的，我用的是：http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz002095&scale=240&ma=no&datalen=250
其中的参数可以改，scale单位是分钟。这个地址数据很全，开盘、收盘、最高、最低、成交量都有，遗憾的是数据不除权。
精确的复权数据，我是从tushare上取的，tushare只支持python，不支持VBA。要是能从你提供的地址直接用VBA取就好了。

新浪财经50ETF期权行情接口
2017-01-12 09:07:41 陆子野 阅读数 10824更多
分类专栏： 金融
版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。
本文链接：https://blog.csdn.net/u013781175/article/details/54374798
1、获得当前有哪几个月份的合约http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName

      返回结果示例如下，contractMonth字段就是我们想要的数据

{
    "result":{
        "status":{
            "code":0
        },
        "data":{
            "cateList":[
                "50ETF",
                "50ETF"
            ],
            "contractMonth":[
                "2019-03",
                "2019-03",
                "2019-04",
                "2019-06",
                "2019-09"
            ],
            "stockId":"510050",
            "cateId":"510050C1903A02400"
        }
    }
}
2、获得某个月份合约的到期日和剩余天数等http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?date=20190901

大家调用的时候把年和月改成上面第一个接口返回的年和月，例如2019年4月就是date=20190401，结果示例如下，expireDay字段为到期日，remainderDays字段为剩余天数

'''
import urllib.request
import re
import time
import ssl
import http.cookiejar
import os

def getHtml(url):
    while True:
        context = ssl._create_unverified_context()
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent','Mozilla/5.0')]
        urllib.request.install_opener(opener)
        try:
            html = urllib.request.urlopen(url, timeout=5).read()
            break
        except:
            print("超时重试")
            time.sleep(3)
    html = html.decode('gbk')
    return html


def getTable(html):
    s = r'(?<=<table class="datatbl" id="datatbl">)([\s\S]*?)(?=</table>)'
    pat = re.compile(s)
    code = pat.findall(html)
    return code


def getTitle(tableString):
    s = r'(?<=<thead)>.*?([\s\S]*?)(?=</thead>)'
    pat = re.compile(s)
    code = pat.findall(tableString)
    s2 = r'(?<=<tr).*?>([\s\S]*?)(?=</tr>)'
    pat2 = re.compile(s2)
    code2 = pat2.findall(code[0])
    s3 = r'(?<=<t[h,d]).*?>([\s\S]*?)(?=</t[h,d]>)'
    pat3 = re.compile(s3)
    code3 = pat3.findall(code2[0])
    return code3


def getBody(tableString):
    s = r'(?<=<tbody)>.*?([\s\S]*?)(?=</tbody>)'
    pat = re.compile(s)
    code = pat.findall(tableString)
    s2 = r'(?<=<tr).*?>([\s\S]*?)(?=</tr>)'
    pat2 = re.compile(s2)
    code2 = pat2.findall(code[0])
    s3 = r'(?<=<t[h,d]).*?>(?!<)([\s\S]*?)(?=</)[^>]*>'
    pat3 = re.compile(s3)
    code3 = []
    for tr in code2:
        code3.append(pat3.findall(tr))
    return code3


def his_daily_mx_from_sina(ticker_symbol, tran_date, temp_save_filename):
    # 股票代码
    symbol = ticker_symbol

    if not os.path.exists(ticker_symbol):       # 判断文件夹是否存在
        os.mkdir(ticker_symbol)                 # 创建文件夹    
    fp = open(ticker_symbol+'\\'+temp_save_filename,'w')

    # 页码，因为不止1页，从第一页开始爬取
    page = 1

    while True:
        Url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + symbol + '&date=' + tran_date + '&page=' + str(page)
        print(Url)
        html = getHtml(Url)
        table = getTable(html)
        if len(table) != 0:
            tbody = getBody(table[0])
            if len(tbody) == 0:
                print("结束")
                break
            if page == 1:
                thead = getTitle(table[0])
                temp_str_td = ''
                for td in thead:
                    td=td.strip()
                    td=td.replace(",","")
                    temp_str_td = temp_str_td + '|' + str(td) 
                temp_str_td = temp_str_td[1:]
                print(temp_str_td)
                fp.writelines(temp_str_td+'\n')

            for tr in tbody:
                temp_str_td = ''
                for td in tr:
                    td=td.strip()
                    td=td.replace(",","")
                    temp_str_td = temp_str_td + '|' + str(td) 
                temp_str_td = temp_str_td[1:]
                print(temp_str_td)
                fp.writelines(temp_str_td+'\n')
            time.sleep(2)
        else:
            print("当日无数据")
            break
        page += 1
    fp.close()

if __name__ == '__main__':
    his_daily_mx_from_sina('sz000063', '2019-11-22', 'sz300063_1122.txt')
