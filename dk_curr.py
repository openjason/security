#-*- coding: utf-8 -*-
#Author: JasonChan
#从sianjs上读取时间，替换本机系统时间
VERSION = "Ver: 20180528 "


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
import logging
import os
import configparser
import time
import datetime
from filecmp import dircmp
import socket
from ctypes import *
import ssl

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import http.cookiejar
from anjian import stock_sale
from anjian import stock_buy

SMTP_SERVER = ""
WORK_DIR = ""
SMTP_USER = ""
SMTP_PWD = ""
SMTP_SENDER = ""

long_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
folder_prefix = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
log_prefix = time.strftime('%m%d', time.localtime(time.time()))

cf = configparser.ConfigParser()
cf_file = 'conf.ini'
if not os.path.isfile(cf_file):
    logging.critical('无法打开配置文件：conf.ini ')
    exit(2)
try:
    cf.read(cf_file, encoding="utf-8-sig")
    target_total = int (cf.get("Common", "total"))
    from_email_addr = cf.get("Common", "from_email_addr")
    SMTP_SERVER = cf.get("Common", "SMTP_SERVER")
    WORK_DIR = cf.get("Common", "WORK_DIR")
    SMTP_USER = cf.get("Common", "SMTP_USER")
    SMTP_PWD = cf.get("Common", "SMTP_PWD")
except:
    logging.warning('无法打开文件 conf.ini 或设置错误.')
    exit(2)

target_name = []
target_httpa = []
target_httpb = []
target_httpc = []
target_id = []
target_dk_flag =[]
target_dk_value = []
target_dk_amount = []
target_emailaddr = []

target_volatility = []
target_timerange = []
target_onduty = []
last_first_price = []
last_secondary_price = []
exchage_done = []


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%a, %d %b %H:%M:%S',
                    filename = os.path.join(WORK_DIR,log_prefix+'.log'),
                    filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

for i in range(1,target_total+1):
    try:
        cfstr = 'Target' + str(i)
        target_name.append(cf.get(cfstr,'name'))
        target_httpa.append(cf.get(cfstr,'httpa'))
        target_httpb.append(cf.get(cfstr,'httpb'))
        target_httpc.append(cf.get(cfstr,'httpc'))
        target_id.append(cf.get(cfstr, 'stock_id'))
        target_dk_flag.append(cf.get(cfstr, 'dk_flag'))
        target_dk_value.append(cf.get(cfstr, 'dk_value'))
        target_dk_amount.append(cf.get(cfstr, 'dk_amount'))
        target_emailaddr.append(cf.get(cfstr,'to_email_addr'))
        target_volatility.append(cf.get(cfstr,'volatility'))
        target_timerange.append(cf.get(cfstr,'timerange'))
        target_onduty.append(cf.get(cfstr,'onduty'))

        #新交易类型，需配置初始值
        if cf.get(cfstr, 'dk_flag') == 'dkbuy' or cf.get(cfstr, 'dk_flag') == 'tpsale':
            last_first_price.append(-7777)
            last_secondary_price.append(-7777)
        else:
            last_first_price.append(8888)
            last_secondary_price.append(8888)

        exchage_done.append(True)

    except:
        logging.warning("conf.ini 配置有误，参数:"+cfstr)



def check_smtp_server(ipaddr,port):
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ipaddr,port))
        sock.close()
        return True
    except socket.error as e:
        sock.close()
        return False

def send_email(toaddr,c_subject):
    logging.info("Subject:"+c_subject)
    toaddr = SMTP_USER
    try:
        msg = MIMEMultipart()
        msg['To'] = ";".join(toaddr)
        msg['From'] = SMTP_SENDER+"<" + SMTP_USER + ">"
        msg['Subject'] = c_subject
        html = c_subject
        html = html.replace("YYYY-MM-DD",long_date)
        body = MIMEText(html, 'plain')
        #    body = MIMEText(text_body, 'plain')
        msg.attach(body)  # add message body (text or html)

        server = smtplib.SMTP(SMTP_SERVER, 25)
        server.login(SMTP_USER, SMTP_PWD)
        mailbody = msg.as_string()

        server.sendmail(SMTP_USER, toaddr, mailbody) #send mail to & cc email address
        logging.info("发送邮件OK："+"to:"+c_subject)
        server.quit()
    except:
        logging.info("error发送邮件："+"to:"+c_subject)

def check_server_auth():
    try:
        server = smtplib.SMTP(SMTP_SERVER, 25)
        server.login(SMTP_USER, SMTP_PWD)
        server.quit()
        return True
    except:
        return False

def clear_files(dir):
    rootdir = dir
    for parent, dirnames, filenames in os.walk(rootdir, False):
        for name in filenames:
            logging.info("移动文件, 文件名为："+parent + '\\'+ name)
            try:
                os.remove(os.path.join(parent, name))
            except:
                logging.warning("移动文件失败文件名为：" + parent + '\\' + name)
                return False
    return True

def getHtml_sinajs(url):
    try:
        context = ssl._create_unverified_context()
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent','Mozilla/5.0')]
        urllib.request.install_opener(opener)
        html_bytes = urllib.request.urlopen(url,context=context).read()
        html_string = html_bytes.decode("gb2312")
        return html_string
    except:
        logging.info("error in getHtml_sinajs(url).")
        return "error."
def get_curr_sinajs(html_doc):
    #is string not need beautifulsoup.
    soup = html_doc
    if len(soup) > 2:
        lstTemp = soup.split('"')
    if len(lstTemp) == 3 :
        strTemp = lstTemp[1]
        lstTemp = strTemp.split(',')

        curr_str = lstTemp[3]
        last_str = lstTemp[2]
        sinajs_time = lstTemp[31]
        gap_float = round(float(curr_str) - float(last_str),3)
        rate = round(gap_float * 100 / float(last_str),2)
        rtstr = curr_str + '|' + str(gap_float) + '|' + str(rate) +'%' + '|' + sinajs_time
        return rtstr
    else:
        logging.info("error in get_curr_sinajs(html_doc)")
        return ("error no data.")
# 这个字符串由许多数据拼接在一起，不同含义的数据用逗号隔开了，按照程序员的思路，顺序号从0开始。
# 0：”大秦铁路”，股票名字；
# 1：”27.55″，今日开盘价；
# 2：”27.25″，昨日收盘价；
# 3：”26.91″，当前价格；
# 4：”27.55″，今日最高价；
# 5：”26.20″，今日最低价；
# 6：”26.91″，竞买价，即“买一”报价；
# 7：”26.92″，竞卖价，即“卖一”报价；
# 8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
# 9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
# 10：”4695″，“买一”申请4695股，即47手；
# 11：”26.91″，“买一”报价；
# 12：”57590″，“买二”
# 13：”26.90″，“买二”
# 14：”14700″，“买三”
# 15：”26.89″，“买三”
# 16：”14300″，“买四”
# 17：”26.88″，“买四”
# 18：”15100″，“买五”
# 19：”26.87″，“买五”
# 20：”3100″，“卖一”申报3100股，即31手；
# 21：”26.92″，“卖一”报价
# (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
# 30：”2008-01-11″，日期；
# 31：”15:05:32″，时间；


def getHtml_baidu(url):
    try:
        context = ssl._create_unverified_context()
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent','Mozilla/5.0')]
        urllib.request.install_opener(opener)
        html_bytes = urllib.request.urlopen(url,context=context).read()
        html_string = html_bytes.decode('utf-8')
        return html_string
    except:
        logging.info("error in getHtml_baidu(url).")
        return "error in getHtml_baidu(url)."

def get_curr_baidu(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    stock_info = soup.find_all(class_ = "price s-up ") #price s-down
    get_text = ""
    if len(stock_info)>0:
        i = stock_info[0]
        get_text = i.get_text()
        if len(get_text)>0:
            get_text = get_text.split()
            rt = get_text[0]+"|"+get_text[1]+"|"+get_text[2]
        return (rt)
    stock_info = soup.find_all(class_="price s-down ")  # price s-down
    get_text = ""
    if len(stock_info) > 0:
        i = stock_info[0]
        get_text = i.get_text()
        if len(get_text) > 0:
            get_text = get_text.split()
            rt = get_text[0]+"|"+get_text[1]+"|"+get_text[2]
        return (rt)
    stock_info = soup.find_all(class_="price s-stop ")  # price s-down
    get_text = ""
    if len(stock_info) > 0:
        i = stock_info[0]
        get_text = i.get_text()
        if len(get_text) > 0:
            get_text = get_text.split()
            rt = get_text[0]+"|"+get_text[1]+"|"+get_text[2]
        return (rt)
    logging.info ("error no data.in get_curr_baidu(html_doc)")
    return ("error no data.in get_curr_baidu(html_doc)")

def get_from_site(httpa,httpb,httpc):
    current_price_str = '2.31 1% 0.02'
    current_price_str = get_current(httpa)
    if 'error' in current_price_str:
        current_price_str = get_current(httpb)
        if 'error' in current_price_str:
            current_price_str = get_current(httpc)
            if 'error' in current_price_str:
                return "error in get_from_site(httpa,httpb,httpc)"
    return current_price_str

def get_current(http):
    if 'baidu' in http:
        baidu_html = getHtml_baidu(http)
        new_price_str = get_curr_baidu(baidu_html)
        return (new_price_str)
    if 'sinajs' in http:
        sianjs_html = getHtml_sinajs(http)
        new_price_str = get_curr_sinajs(sianjs_html)
        return (new_price_str)
    return "error in get_current(http)."


#对目标进行轮询,检测当前价格与设定dk价格进行比较,如最新价及上两次价格都满足条件,则进行交易操作.
#对目标dk值设置采用相反的比较,符合条件(差为正)则执行操作.否则记录更新上两次价格.
def dk_detect():
    global exchage_done
    global target_total
    global target_dk_value
    global target_dk_amount
    global target_dk_flag
    global target_httpa
    global target_httpb
    global target_httpc
    global target_id
    global last_first_price
    global last_secondary_price

    for i in range(target_total):
    #标号 数字 显示 从 1 开始，与配置文件一致，读取配置文件标号已做处理 。
        httpa = target_httpa[i]
        httpb = target_httpb[i]
        httpc = target_httpc[i]
        dk_flag = target_dk_flag[i]
        dk_value = float(target_dk_value[i])
        dk_amount = int(target_dk_amount[i])
        id = target_id [i]

        last_one_value = last_first_price[i]
        last_two_value = last_secondary_price[i]

        time.sleep(1.7)
        new_price_str_raw = get_from_site(httpa,httpb,httpc)

        if "|" in new_price_str_raw:
            new_price_str = new_price_str_raw.split('|')
        else:
            new_price_str = []
        dk_gap = -888888
        try:
            new_price = round(float(new_price_str[0]), 3)
            updown_pice = new_price_str[1]
            updown_rate = new_price_str[2]
            web_time = new_price_str[3]
        except:
            logging.info("gap get error.")
            continue

        if dk_flag == 'dkbuy':
            #计划买入,之前价格检测２次均符合条件，执行交易
            dk_gap = round(new_price - dk_value,3)
            if (dk_gap >0) and (last_one_value - dk_value) > 0 and (last_two_value - dk_value) >0:
                if exchage_done[i] and is_exchage_time(i):
                    logging.info ("Excute exchage......" + id + dk_flag+":" +str(dk_amount))
                    stock_buy(id,str(dk_amount))
                    exchage_done[i] = False
                    send_email(SMTP_USER,"DK Message:"+str(id) + str(new_price_str)+dk_flag+str(dk_amount))
            else:
                last_secondary_price[i] = last_first_price[i]
                last_first_price[i] = new_price
        #end of dkbuy

        elif dk_flag == 'tpbuy': ##到目标价，买
            dk_gap = round(dk_value - new_price, 3)
            if (dk_gap >0) and (dk_value - last_one_value ) > 0 and (dk_value - last_two_value ) >0:
                if exchage_done[i] and is_exchage_time(i):
                    logging.info ("Excute exchage......" + id + dk_flag+":" +str(dk_amount))
                    stock_buy(id,str(dk_amount))
                    exchage_done[i] = False
                    send_email(SMTP_USER,"DK Message:"+str(id) + str(new_price_str)+dk_flag+str(dk_amount))
            else:
                last_secondary_price[i] = last_first_price[i]
                last_first_price[i] = new_price
        #end of tpbuy

        elif dk_flag == 'dksale':
            #计划卖出，之前价格检测２次均符合条件，执行交易
            dk_gap = round(dk_value - new_price, 3)
            if (dk_gap >0) and (dk_value - last_one_value ) > 0 and (dk_value - last_two_value ) >0:
                if exchage_done[i] and is_exchage_time(i):
                    logging.info ("Excute exchage......" + id + dk_flag+":" +str(dk_amount))
                    stock_sale(id,str(dk_amount))
                    exchage_done[i] = False
                    send_email(SMTP_USER,"DK Message:"+str(id) + str(new_price_str)+dk_flag+str(dk_amount))
            else:
                last_secondary_price[i] = last_first_price[i]
                last_first_price[i] = new_price
        #end of dksale

        elif dk_flag == 'tpsale':   #到目标价，卖
            dk_gap = round(new_price - dk_value,3)
            if (dk_gap >0) and (last_one_value - dk_value) > 0 and (last_two_value - dk_value) >0:
                if exchage_done[i] and is_exchage_time(i):
                    logging.info ("Excute exchage......" + id + dk_flag + ":" +str(dk_amount))
                    stock_sale(id,str(dk_amount))
                    exchage_done[i] = False
                    send_email(SMTP_USER,"DK Message:"+str(id) + str(new_price_str)+dk_flag+str(dk_amount))
            else:
                last_secondary_price[i] = last_first_price[i]
                last_first_price[i] = new_price
        #end of tpsale
        else:
            logging.info ("无此交易类型...error.")


        #记录全部交易类型的日志。
        logging.info(str(id)+"@"+web_time+"$"+ str(new_price)+'|'+str(updown_pice)+"|"+str(updown_rate)+"|"+dk_flag+"_"+str(dk_amount)\
            +"|"+str(dk_value)+" gap:"+str(dk_gap) + "|"+str(last_one_value) + "|"+str(last_two_value))
        continue
    return 0

def show_setting():
    for i in range(target_total):
    #标号 数字 显示 从 1 开始，与配置文件一致，读取配置文件标号已做处理 。
        httpa = target_httpa[i]
        httpb = target_httpb[i]
        httpc = target_httpc[i]
        dk_flag = target_dk_flag[i]
        dk_value = float(target_dk_value[i])
        dk_amount = int(target_dk_amount[i])
        id = target_id [i]

        print(str(i + 1) + ":" + str(id) + "|" + " " + "|" + dk_flag + "_" + str(dk_amount) + " value:"
              + str(dk_value) + "|" + str(httpa) + "|" + str(httpb))

def is_exchage_time(i):
    str_time = time.strftime('%Y%m%d %H%M%S', time.localtime(time.time()))
    if (int(str_time[9:16]) in range(92700, 113800) or int(str_time[9:16]) in range(125700, 150800)):
        return True
    else:
        logging.info(str_time + " error, out of exchange time.")
        return False

if __name__ == "__main__":
    logging.info(VERSION)
    show_setting()
    while (True):
        str_time = time.strftime('%Y%m%d %H%M%S', time.localtime(time.time()))
        time.sleep(0.1)
        print (str_time[9:],flush=True)
        if (int(str_time[9:16]) in range(52800, 160800)):
            dk_detect()
        else:
            print("out of exchange time.")
            time.sleep(14)
