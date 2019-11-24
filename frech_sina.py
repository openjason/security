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
