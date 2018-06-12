#!/usr/bin/python3
# Author: Jason Chan

VERSION = "Ver: 2018060905"

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
import queue
import threading
from anjian import stock_sale
from anjian import stock_buy


long_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
folder_prefix = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
log_prefix = time.strftime('%m%d', time.localtime(time.time()))

common_configure = {} # a dict
target_configure = [] # a list ,some dict in it.

exitFlag = 0

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%a, %d %b %H:%M:%S',
                    filename = log_prefix+'.log',
                    filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)


def read_configure(conf_name= 'conf.ini'):
    cf = configparser.ConfigParser()
    cf_file = conf_name
    if not os.path.isfile(cf_file):
        logging.critical('无法打开配置文件：conf.ini ')
        exit(2)
    try:
        cf.read(cf_file, encoding="utf-8-sig")
        common_configure['total'] = int(cf.get("Common", "total"))
        common_configure['from_email_addr'] = cf.get("Common", "from_email_addr")
        common_configure['SMTP_SERVER'] = cf.get("Common", "SMTP_SERVER")
        common_configure['WORK_DIR'] = cf.get("Common", "WORK_DIR")
        common_configure['SMTP_USER'] = cf.get("Common", "SMTP_USER")
        common_configure['SMTP_PWD'] = cf.get("Common", "SMTP_PWD")
    except Exception as e:
        logging.warning('无法打开文件 conf.ini 或设置错误.')
        logging.warning(e)
        exit(2)

    for i in range(1, common_configure['total'] + 1):
        target_dict = {}
        try:
            cfstr = 'Target' + str(i)
            target_dict['name'] = cf.get(cfstr, 'name')
            target_dict['httpa'] = cf.get(cfstr, 'httpa')
            target_dict['httpb'] = cf.get(cfstr, 'httpb')
            target_dict['httpc'] = cf.get(cfstr, 'httpc')
            target_dict['stock_id'] = cf.get(cfstr, 'stock_id')
            target_dict['dk_flag'] = cf.get(cfstr, 'dk_flag')
            target_dict['dk_value'] = cf.get(cfstr, 'dk_value')
            target_dict['dk_amount'] = cf.get(cfstr, 'dk_amount')
            target_dict['to_email_addr'] = cf.get(cfstr, 'to_email_addr')
            target_dict['volatility'] = cf.get(cfstr, 'volatility')
            target_dict['timerange'] = cf.get(cfstr, 'timerange')
            target_dict['onduty'] = cf.get(cfstr, 'onduty')
            target_configure.append(target_dict)

            # 新交易类型，需配置初始值
            # if cf.get(cfstr, 'dk_flag') == 'dkbuy' or cf.get(cfstr, 'dk_flag') == 'tpsale':
            #     last_first_price.append(-7777)
            #     last_secondary_price.append(-7777)
            # else:
            #     last_first_price.append(8888)
            #     last_secondary_price.append(8888)
            #
            # exchage_done.append(True)
        except Exception as e:
            logging.warning("conf.ini 配置有误，参数:" + cfstr)
            logging.warning(e)
            exit(2)

def show_setting():
    print(common_configure)
    for i in range(common_configure['total']):
    #标号 数字 显示 从 1 开始，与配置文件一致，读取配置文件标号已做处理 。
        print("= " * 35)
        for tdict in target_configure[i]:
            print ("%15s : %-60s"%(tdict,target_configure[i][tdict]))
    print("= "*35)

def send_email(toaddr,c_subject):
    logging.info("Subject:"+c_subject)
#    toaddr = toaddr
    try:
        msg = MIMEMultipart()
        msg['To'] = ";".join(toaddr)
        msg['From'] = "Jason<" + common_configure['SMTP_USER'] + ">"
        msg['Subject'] = c_subject
        html = c_subject
        body = MIMEText(html, 'plain')
        #    body = MIMEText(text_body, 'plain')
        msg.attach(body)  # add message body (text or html)

        server = smtplib.SMTP(common_configure['SMTP_SERVER'], 25)
        server.login(common_configure['SMTP_USER'], common_configure['SMTP_PWD'])
        mailbody = msg.as_string()

        server.sendmail(common_configure['SMTP_USER'], toaddr, mailbody) #send mail to & cc email address
        logging.info("发送邮件OK："+"to:"+toaddr + " Subj:"+c_subject)
        server.quit()
    except Exception as e:
        logging.info("error发送邮件："+"to:"+toaddr + " Subj:"+c_subject)
        logging.info(e)


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
        lenghtofstr=len(lstTemp)
        if lenghtofstr == 33:
            return strTemp
    logging.info("error in get_curr_sinajs(html_doc).")
    return ("error in get_curr_sinajs(html_doc).")
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

def update_price_queue(threadID, dict_target, security_stat, price_queue):
    i = threadID
    # 标号 数字 显示 从 1 开始，与配置文件一致，读取配置文件标号已做处理 。
    httpa = dict_target['httpa']
    # httpb = dict_target['httpb']
    # httpc = dict_target['httpc']
    httpb = ''
    httpc = ''
    # only use sinajs data

    dk_flag = dict_target['dk_flag']
    dk_value = float(dict_target['dk_value'])
    dk_amount = int(dict_target['dk_amount'])
    id = dict_target['stock_id']

    new_price_str_raw = get_from_site(httpa, httpb, httpc)

    print(new_price_str_raw)
    new_price_str_lst = new_price_str_raw.split(',')
    print(new_price_str_lst)
    try:
        new_price = float(new_price_str_lst[3])
        updown_pice = float(new_price_str[1])
        updown_rate = new_price_str[2]
        web_time = new_price_str[3]
    except:
        logging.info("update price queue error.")
        return ("error. update price queue error.")
    if dk_flag == 'dkbuy':
        # 计划买入,之前价格检测２次均符合条件，执行交易
        dk_gap = round(new_price - dk_value, 3)

    elif dk_flag == 'tpbuy':  ##到目标价，买
        dk_gap = round(dk_value - new_price, 3)

    elif dk_flag == 'dksale':
        # 计划卖出，之前价格检测２次均符合条件，执行交易
        dk_gap = round(dk_value - new_price, 3)

    elif dk_flag == 'tpsale':  # 到目标价，卖
        dk_gap = round(new_price - dk_value, 3)
    price_queue.pop(0)
    price_queue.append(new_price)

    # 记录全部交易类型的日志。
    logging.info(str(id) + "@" + web_time + "$" + str(new_price) + '|' + str(updown_rate) + "|" + str(
        updown_pice) + "|" + dk_flag + "_" + str(dk_amount) \
                 + "|" + str(dk_value) + " gap:" + str(dk_gap) + str(price_queue))


def dk_check(threadID, dict_target, security_stat, price_queue):
    string_return = 'not ok'
    i = threadID
    #标号 数字 显示 从 1 开始，与配置文件一致，读取配置文件标号已做处理 。
    dk_flag = dict_target['dk_flag']
    dk_value = float(dict_target['dk_value'])
    dk_amount = int(dict_target['dk_amount'])
    id = dict_target['stock_id']

    last_one_value = price_queue[-2]
    last_two_value = price_queue[-3]
#    print('jt1:',last_one_value,last_two_value)

    dk_gap = -888888
    try:
        new_price = price_queue[-1]
        updown_pice = new_price_str[1]
        updown_rate = new_price_str[2]
        web_time = new_price_str[3]
    except:
        logging.info("gap get error.")

    if dk_flag == 'dkbuy':
        #计划买入,之前价格检测２次均符合条件，执行交易
        dk_gap = round(new_price - dk_value,3)
        if in_range_of_price(new_price,dk_gap):
            if (dk_gap >0) and (last_one_value - dk_value) > 0 and (last_two_value - dk_value) >0:
                string_return = 'dk_fitted'
    #end of dkbuy

    elif dk_flag == 'tpbuy': ##到目标价，买
        dk_gap = round(dk_value - new_price, 3)
        if in_range_of_price(new_price,dk_gap):
            if (dk_gap >0) and (dk_value - last_one_value ) > 0 and (dk_value - last_two_value ) >0:
                string_return= 'dk_fitted'
    #end of tpbuy

    elif dk_flag == 'dksale':
        #计划卖出，之前价格检测２次均符合条件，执行交易
        dk_gap = round(dk_value - new_price, 3)
        if in_range_of_price(new_price, dk_gap):
            if (dk_gap >0) and (dk_value - last_one_value ) > 0 and (dk_value - last_two_value ) >0:
                string_return= 'dk_fitted'

    #end of dksale

    elif dk_flag == 'tpsale':   #到目标价，卖
        dk_gap = round(new_price - dk_value,3)
        if in_range_of_price(new_price, dk_gap):
            if (dk_gap >0) and (last_one_value - dk_value) > 0 and (last_two_value - dk_value) >0:
                string_return= 'dk_fitted'
    #end of tpsale
    else:
        logging.info ("无此交易类型...error.")
    price_queue.pop(0)
    price_queue.append(new_price)

    #记录全部交易类型的日志。
    logging.info(str(id)+"@"+web_time+"$"+ str(new_price)+'|'+str(updown_rate)+"|"+str(updown_pice)+"|"+dk_flag+"_"+str(dk_amount)\
        +"|"+str(dk_value)+" gap:"+str(dk_gap) + str(price_queue))

    return string_return


def in_exchage_time(stock_id_str):
    str_time = time.strftime('%Y%m%d %H%M%S', time.localtime(time.time()))
    if (int(str_time[9:16]) in range(92700, 113800) or int(str_time[9:16]) in range(125700, 150800)):
        return True
    else:
        logging.info(str_time + " error, out of exchange time.id = %s",stock_id_str)
        return False

def in_range_of_price(value,gap):
    if abs(gap) < (value * 0.11):
        return True
    else:
        logging.info('Out of 10% range.price = %s',value)
        return False

def n_elements_average(my_list, n):
    n_e_aver = [sum(my_list[k: k + n]) / float(len(my_list[k: k + n]))for k in range(0, len(my_list), n)]
    return n_e_aver

def slope_of_price(my_list):
    #
    average_list = n_elements_average(my_list,4)
    if average_list[0] != 0 and average_list[1] != 0:
        slope_o_p = average_list [0]/average_list[1]
    else:
        slope_o_p = 0
    return slope_o_p

class SecurityThread (threading.Thread):
    def __init__(self, threadID, dict_target, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.dict_target = dict_target
        self.security_stat = {'exchage_done':False}
        self.price_queue = [0,0,0,0,0,0,0,0,0,0]
        self.q = q
    def run(self):
        logging.info ("开启线程：" + self.dict_target['name'])
        while(True):
            logging.info(n_elements_average(self.price_queue,3))
            logging.info(slope_of_price(self.price_queue))
            update_price_queue(self.threadID, self.dict_target,self.security_stat,self.price_queue)
            time.sleep(3)
            continue

            if dk_check(self.threadID, self.dict_target,self.security_stat,self.price_queue) == 'dk_fitted':
                if self.dict_target['onduty'] == 'F':
                    logging.info('dk_fitted: '+ self.dict_target['stock_id'] + ' but onduty is False.')
                    time.sleep(3)
                    continue
                logging.info('dk_fitted: '+ self.dict_target['stock_id'])
                if (not self.security_stat['exchage_done']) and in_exchage_time(self.dict_target['stock_id']):
                    logging.info('time is ok, ready for do it...')
                    if 'buy' in self.dict_target['dk_flag']:
                        logging.info('dk_buy_signal...')
                        self.security_stat['exchage_done'] = True
#                        continue
                        # locker for exchage，only one exchage can be excute at once..
                        threadLock.acquire()
                        stock_buy(self.dict_target['stock_id'],self.dict_target['dk_amount'])
                        threadLock.release()

                        message_email = "DK Message:"+self.dict_target['stock_id'] + str(self.price_queue[9])+self.dict_target['dk_flag']+str(self.dict_target['dk_amount'])
                        send_email(self.dict_target['to_email_addr'],message_email)

                    elif 'sale' in self.dict_target['dk_flag']:
                        logging.info('dk_sale_signal...')
                        self.security_stat['exchage_done'] = True
#                        continue
                        # locker for exchage，only one exchage can be excute at once..
                        threadLock.acquire()
                        stock_sale(self.dict_target['stock_id'],self.dict_target['dk_amount'])
                        threadLock.release()
                        message_email = "DK Message:"+self.dict_target['stock_id'] + str(self.price_queue[9])+self.dict_target['dk_flag']+str(self.dict_target['dk_amount'])
                        send_email(self.dict_target['to_email_addr'],message_email)
                    else:
                        logging.error('error, wrong dk_flag',target_configure['dk_flag'])

            time.sleep(3)
        logging.info ("退出线程：" + self.dict_target['name'])

if __name__ == '__main__':
    read_configure('conf.ini')
    show_setting()

#    send_email('13825686039@139.com','test for dk')
#    exit(0)
    # threadList = target_id
    # nameList = target_name
    queueLock = threading.Lock()
    exchange_Queue = queue.Queue(10)
    threads = []
    threadID = 0

    # 创建新线程
    for int_list_id in range(common_configure['total']):
        #print(int_list_id,threadID[int_list_id])
        thread = SecurityThread(threadID, target_configure[int_list_id], exchange_Queue)
        thread.daemon = True
        thread.start()
        # try:
        #     while thread.isAlive():
        #         pass
        # except KeyboardInterrupt:
        #     print('stopped by keyboard')
        # print('main end')
        threads.append(thread)
        threadID += 1

    threadLock = threading.Lock()
    # 填充队列
#    queueLock.acquire()
    # for word in nameList:
    #     exchange_Queue.put(word)
#    queueLock.release()

    # 等待队列清空
#    while not exchange_Queue.empty():
#        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    # for t in threads:
    #     t.join()
    # logging.info("退出主线程")

    #set thread deamon , then keep main func alive. not use join().
    while True:
        time.sleep(1)