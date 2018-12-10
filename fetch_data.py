import sina_his
import todb
import datetime
import time

def run_gethis_todb(curr_stock,curr_date,curr_filename):
    dairy_data = sina_his.Getdailydata()
    if 0 == dairy_data.his_daily_from_sina(curr_stock, curr_date, curr_filename):#正常完成读取数据结束
        time.sleep(1)
        todb.writetodb(curr_filename)


if __name__ == '__main__':

    curr_stock = 'sz300750'

    date_begin = datetime.datetime(2018,9,7)
    for i in range(33):
        # Monday is 0 and Sunday is 6.
        if date_begin.isoweekday() < 6:
            curr_date = str(date_begin.strftime('%Y-%m-%d'))
            curr_filename = curr_stock+'_'+curr_date[5:]+'.log'
            run_gethis_todb(curr_stock,curr_date,curr_filename)
        else:
            print(curr_date + ' is weekend..')

        date_begin = date_begin - datetime.timedelta(days=1)
