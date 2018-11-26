import urllib.request
import re
import time
import ssl
import http.cookiejar


class Getdailydata:
    def __init__(self):
        pass

    def getHtml(self,url):
        while True:
            context = ssl._create_unverified_context()
            cj = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-Agent','Mozilla/5.0')]
            urllib.request.install_opener(opener)
            try:
                html = urllib.request.urlopen(url, timeout=3).read()
                break
            except:
                print("超时重试")
                time.sleep(7)
        html = html.decode('gbk')
        return html


    def getTable(self,html):
        s = r'(?<=<table class="datatbl" id="datatbl">)([\s\S]*?)(?=</table>)'
        pat = re.compile(s)
        code = pat.findall(html)
        return code


    def getTitle(self, tableString):
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


    def getBody(self, tableString):
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


    def his_daily_from_sina(self, ticker_symbol, tran_date, temp_save_filename):
        # 股票代码
        symbol = 'sz300750'
        # 日期
    #    dateObj = datetime.datetime(2018, 8, 31)
        #tran_date = dateObj.strftime("%Y-%m-%d")

        fp = open(temp_save_filename,'w',encoding='UTF-8')

        # 页码，因为不止1页，从第一页开始爬取
        page = 1

        while True:
            Url = 'http://market.finance.sina.com.cn/transHis.php?symbol=' + symbol + '&date=' + tran_date + '&page=' + str(page)
            html = self.getHtml(Url)
            table = self.getTable(html)
            if len(table) != 0:
                tbody = self.getBody(table[0])
                if len(tbody) == 0:
                    print("结束")
                    break
                if page == 1:
                    thead = self.getTitle(table[0])
                    print(thead)
                    #fp.writelines(str(thead)+'\n')
                for tr in tbody:
                    print(tr)
                    itemcount = 0
                    fp.write(tran_date)
                    for item in tr:
                        if itemcount > 0:
                            fp.write(',')
                        fp.write(item)
                        itemcount = itemcount + 1;
                    fp.write('\n')
                time.sleep(4)
            else:
                print("当日无数据")
                break
            page += 1
        fp.close()

if __name__ == '__main__':
    test = Getdailydata()
    test.his_daily_from_sina('sz300750', '2018-11-22', 'sz300750_1122.log')
