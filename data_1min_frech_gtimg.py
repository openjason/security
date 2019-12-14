#！/bin/python
'''
#http://data.gtimg.cn/flashdata/hushen/minute/sz000063.js?maxage=110&0.28163905744440854
http://data.gtimg.cn/flashdata/hushen/4day/sz/sz300059.js

'''
import urllib.request
import re
import time
import ssl
import http.cookiejar
import os
import json

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


def his_daily_1m_from_htimg(ticker_symbol, tran_date, temp_save_filename):
    # 股票代码
    symbol = ticker_symbol

    if not os.path.exists(ticker_symbol):       # 判断文件夹是否存在
        os.mkdir(ticker_symbol)                 # 创建文件夹    
    fp = open(ticker_symbol+'\\'+temp_save_filename,'w')

    # 页码，因为不止1页，从第一页开始爬取
    page = 1

    Url = 'http://data.gtimg.cn/flashdata/hushen/4day/sz/sz300059.js'
    print(Url)
    html = getHtml(Url)
    htmllist = html.split('=')
    table = htmllist[1]
    if table[-1]==';':
        table = table[:-1]
        
    four_days_str = str(eval(table))
    print(type (four_days_str))
    one_day_str = four_days_str[0]
    
    one_day_json = json.loads(four_days_str[0])


    print(one_day_jason['date'])
    print(one_day_jason['data'])
           
    fp.close()

if __name__ == '__main__':
    his_daily_1m_from_htimg('sz000063', '2019-11-22', 'sz300063_1122.txt')
