'''
股票就是估票，决定结果看的是执行力。20181228
处于低潮的2018.
'''

import pymysql.cursors
import datetime,time
import matplotlib.pyplot as plt
import conf



import logging

long_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
folder_prefix = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
log_prefix = time.strftime('%m%d', time.localtime(time.time()))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%a, %d %b %H:%M:%S',
                    filename = log_prefix+'.log',
                    filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)

def xch_one_day(stock,curr_date):

    connection = pymysql.connect(host=conf.DBhost,
                                 user=conf.DBuser,
                                 password=conf.DBpassword,
                                 db=conf.DBname,
                                 cursorclass=pymysql.cursors.DictCursor)
    datalist = []
    try:
        with connection.cursor() as cursor:
            sql = "select * from "+stock+" where xdate > '" + curr_date + " 09:00' and xdate < '" +curr_date + " 16:00' order by xdate"
            #logging.info (sql)
            cursor.execute(sql)

            results = cursor.fetchall()
            datalist = []
            for row in results:
                one_rec = []
                one_rec.append(row['xdate'])
                one_rec.append(row['price'])
                one_rec.append(row['pdiff'])
                one_rec.append(row['volume'])
                one_rec.append(row['amount'])
                one_rec.append(row['bors'])
                datalist.append(one_rec)
                # 打印结果
    except Exception as e:
        print('Error in record,  exit(2)')
        print(e)
        connection.close()
        exit(2)

    connection.commit()
    connection.close()
#    print(datalist)
    return (datalist)


def takeSecond(elem):
    return elem[1]  #按价格大小排序
def sort_segmentation(daylist):
    daylist.sort(key=takeSecond)
    print('first 5 record: ',daylist[:5])
    print('last 5 record: ',daylist[-5:])

def timestamp(timestep):

    time_step_point = datetime.datetime(2000,1,1,9,30,0,0)
    endingtime = datetime.datetime(2000,1,1,15,1)
    timestampdict = {}
    while time_step_point < endingtime:
        tmp_str = time_step_point.strftime('%H%M')
        timestampdict[tmp_str] = 0
        time_step_point = time_step_point + datetime.timedelta(minutes=timestep)
    return (timestampdict)


def statics(timestamp,daylist):
    pass


def list_segmentation(daylist,xdate,timestep):
    #timestep 单位 分钟
    xdate_y = int(xdate[:4])
    xdate_m = int(xdate[5:7])
    xdate_d = int(xdate[8:10])
    #年月日 字符串 转 数字
    segmentation_list = []
    segm_templist = []
    time_step_point = datetime.datetime(xdate_y,xdate_m,xdate_d,9,30,0,0)
    segm_amount = 0
    segm_volum =0
    segm_price = 0
    segm_count = 0
    for indx_rec in range(len(daylist)):
        curr_rec = daylist[indx_rec]
        if curr_rec[0] > time_step_point:
#            print('================================')
#            print(curr_rec)
            segm_count = segm_count + 1
            segm_price = segm_price + curr_rec[1]
            segm_volum = segm_volum + curr_rec[3]
            segm_amount = segm_amount + curr_rec[4]
            segm_templist.append(time_step_point)
            segm_templist.append(segm_price/segm_count)
            segm_templist.append(segm_volum)
            segm_templist.append(segm_amount)
            segmentation_list.append(segm_templist)

            time_step_point = time_step_point + datetime.timedelta(minutes=timestep)
            segm_amount = 0
            segm_volum = 0
            segm_price = 0
            segm_count = 0
            segm_templist = []
        else:
#            print(curr_rec)
            segm_count = segm_count + 1
            segm_price = segm_price + curr_rec[1]
            segm_volum = segm_volum + curr_rec[3]
            segm_amount = segm_amount + curr_rec[4]

    print(segmentation_list)
    return (segmentation_list)

def show_plt(showlist, position):
    rec_list = []
    for rec_one in range(len(showlist)):
        rec_list.append(showlist[rec_one][position])
    print("rec_list: ",rec_list)

    plt.plot(rec_list)
    plt.show()


def get_segmentation(daylist,xdate,xtime,timestep):
    #功能：在daylist列表上计算在xdate（须与daylist对应）xtime（timestep分钟内）交易金额
    #返回-金额-交易记录数-交易数量-交易总额 return (segm_price, segm_count, segm_volum, segm_amount)
    #timestep 单位 分钟
    xdate_y = int(xdate[:4])
    xdate_m = int(xdate[5:7])
    xdate_d = int(xdate[8:10])
    xtime_h = int(xtime[:2])
    xtime_m = int(xtime[-2:])
    #年月日 字符串 转 数字
    segmentation_list = []
    segm_templist = []
    time_step_point = datetime.datetime(xdate_y,xdate_m,xdate_d,xtime_h,xtime_m)
    segm_amount = 0
    segm_volum =0
    segm_price = 0
    segm_count = 0
    for indx_rec in range(len(daylist)):
        curr_rec = daylist[indx_rec]
        if curr_rec[0] > time_step_point:
#            print('================================')
#            print(curr_rec)
            segm_count = segm_count + 1
            segm_price = segm_price + curr_rec[1]
            segm_volum = segm_volum + curr_rec[3]
            segm_amount = segm_amount + curr_rec[4]
            if curr_rec[0] > time_step_point + datetime.timedelta(minutes=timestep):
                break

    if segm_price == 0:
        segm_count = 1
    return (segm_price/segm_count,segm_count,segm_volum,segm_amount)

def fix_time_xch_result(stock,xdatestr,periodicity,xch_time1,xch_time2,timestep):
    #功能： stock号码在xdatestr日开始periodicity日，在xch_time时间（timestep分钟内）交易金额
    #stock  股票代码
    #xdate  交易开始日期
    #periodicity 时间周期，以日为单位，如7日
    #buytime 购买时间，HH:MM
    #saletime 卖出时间，HH:MM
    #timelast 买入卖出时间延续，以分钟为单位
    bigger12 = 0
    bigger21 = 0
    curr_stock = 'sz300750'
    xdate_year = int(xdatestr[:4])
    xdate_month = int(xdatestr[5:7])
    xdate_day = int(xdatestr[8:10])
    date_begin = datetime.datetime(xdate_year,xdate_month,xdate_day)
    for rec_num in range(periodicity):
        if date_begin.isoweekday() > 5:
            #print('Weekend, no xchange at: ' + str(date_begin.strftime('%Y-%m-%d')))
            date_begin = date_begin + datetime.timedelta(days=1)
            continue
        curr_xdatestr = str(date_begin.strftime('%Y-%m-%d'))
        date_begin = date_begin + datetime.timedelta(days=1)#计算当前交易日后自加 1

        daylist = xch_one_day(curr_stock, curr_xdatestr)
#        print(len(daylist))
        if len(daylist) > 0:
            daylist.sort()
            segm_price1, segm_count1, segm_volum1, segm_amount1 = get_segmentation(daylist,curr_xdatestr,xch_time1,timestep)
            segm_price2, segm_count2, segm_volum2, segm_amount2 = get_segmentation(daylist,curr_xdatestr,xch_time2,timestep)
            print (rec_num,':',curr_stock,curr_xdatestr,segm_price1,segm_price2,' split:',segm_price1-segm_price2,)
            if segm_price1 > 0:
                if segm_price1 > segm_price2:
                    bigger12 = bigger12 +1
                else:
                    bigger21 = bigger21 +1

    print('bigger12: ',bigger12,'bigger21: ',bigger21)

if __name__ == '__main__':

    print('Connecting to the database...' + conf.DBuser + '@' + conf.DBhost)
    curr_stock = 'sz300750'
    xdatestr = '2018-07-19'
    timestep = 5
    fix_time_xch_result(curr_stock,xdatestr,160,'09:55','13:30',timestep)

    exit(0)
    daylist = xch_one_day(curr_stock, xdatestr)
    daylist.sort()

    timestampdict = timestamp(timestep)

    print ('one rec: ',type(daylist))
    segm_list3m = list_segmentation(daylist,xdate,timestep)

    show_plt(segm_list3m,1)

    sort_segmentation(segm_list3m)
