#下载一个时间段内每日股票的交易明细；

import datetime
from frech_sina import his_daily_mx_from_sina 


if __name__ == '__main__':

    curr_stock = 'sz000063'

    date_begin = datetime.datetime(2019,11,19)
    date_end = datetime.datetime(2019,11,26)
    for i in range(365):
        # Monday is 0 and Sunday is 6.
        curr_date = str(date_begin.strftime('%Y-%m-%d'))
        if date_begin.isoweekday() < 6:
            curr_filename = curr_stock+'_'+curr_date+'.log'
            print(curr_filename)
            his_daily_mx_from_sina(curr_stock,curr_date,curr_filename)
        else:
            print(curr_date + ' is weekend..')

        date_begin = date_begin + datetime.timedelta(days=1)
        if date_begin > date_end:
            print("time is over. ",date_end)
            break
            
