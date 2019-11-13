#获取股票日线数据
#http://quotes.money.163.com/trade/lsjysj_000063.html#01b07
#http://quotes.money.163.com/trade/lsjysj_000063.html?year=2019&season=4
import urllib.request
import re
import time
import ssl
import http.cookiejar

def getHtml(url):
    while True:
        context = ssl._create_unverified_context()
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64)')]
        urllib.request.install_opener(opener)
        try:
            print(url)
            html = urllib.request.urlopen(url, timeout=5).read()
            break
        except:
            print("超时重试")
            time.sleep(3)
    #html = html.decode('utf-8')
    return html


def getTable(html):
    s = r'(?<=<table class="table_bg001 border_box limit_sale">)([\s\S]*?)(?=</table>)'
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
    s = r'(?<=</thead)>.*?([\s\S]*?)(?=</tr></tr>)'
    pat = re.compile(s)
    code = pat.findall(tableString)
    code[0] = code[0] + '</tr></tr>' # 因为上面的表达是不包含此串，导致字符没有完整，加上，正则可返回匹配串？
    s2 = r'(?<=<tr).*?>([\s\S]*?)(?=</tr>)'
    pat2 = re.compile(s2)
    code2 = pat2.findall(code[0])
    s3 = r'(?<=<t[h,d]).*?>(?!<)([\s\S]*?)(?=</)[^>]*>'
    pat3 = re.compile(s3)
    code3 = []
    for tr in code2:
        code3.append(pat3.findall(tr))
    return code3


def his_daily_from_163(ticker_symbol, tran_date, temp_save_filename):
    # 股票代码
    symbol = ticker_symbol
    fp = open(temp_save_filename,'w')
    # 页码，因为不止1页，从第一页开始爬取
    season = 1 #4 季度，爬4次
    while season < 5:
        Url = 'http://quotes.money.163.com/trade/lsjysj_' + symbol + '.html?year=' + tran_date + '&season=' + str(season)
        #http: // quotes.money.163.com / trade / lsjysj_000063.html?year = 2019 & season = 4
        html = getHtml(Url).decode('utf-8')
        with open('html_temp.log','w',encoding='utf-8') as out_put_file:
            out_put_file.write(html)
        table = getTable(html)
        if len(table) != 0:
            tbody = getBody(table[0])
            if len(tbody) == 0:
                print("结束")
                break
            tbody.reverse() #列表倒置，按时间排序
            #if season == 1:#表头 无用
            #    thead = getTitle(table[0])
            #    print(thead)
            #    fp.writelines(str(thead)+'\n')
            for tr in tbody:
                print(tr)
                fp.writelines(str(tr)+'\n')
            time.sleep(2)
        else:
            print("无数据")
            break
        season += 1
    fp.close()

if __name__ == '__main__':
    his_daily_from_163('300059', '2018', '300059_2010.log')