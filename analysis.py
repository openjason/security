'''


'''

import pymysql.cursors
import datetime
import matplotlib.pyplot as plt


DBhost='1.1.1.177'
#DBhost='192.168.18.101'
DBuser='jcc'
DBpassword='pwd123456'
DBname='stock'

def xch_one_day(stock,curr_date):

    connection = pymysql.connect(host=DBhost,
                                 user=DBuser,
                                 password=DBpassword,
                                 db=DBname,
                                 cursorclass=pymysql.cursors.DictCursor)
    datalist = []
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "select * from "+stock+" where xdate > '" + curr_date + " 09:00' and xdate < '" +curr_date + " 16:00' order by xdate"
            print (sql)
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
        tmp_str = time_step_point.strftime('%m%s')
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


if __name__ == '__main__':

    curr_stock = 'sz300750'
    xdate = '2018-12-11'
    print('Connecting to the database...' + DBuser + '@' + DBhost)
    daylist = xch_one_day(curr_stock, xdate)
    daylist.sort()
    timestep = 5

    timestampdict = timestamp(timestep)

    print ('one rec: ',type(daylist))
    segm_list3m = list_segmentation(daylist,xdate,timestep)

    show_plt(segm_list3m,1)

    sort_segmentation(segm_list3m)
