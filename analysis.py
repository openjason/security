'''


'''

import pymysql.cursors
#import string

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
            sql = "select * from "+stock+" where xdate > '" + curr_date + " 00:00' and xdate < '" +curr_date + " 23:00'"
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
                print(one_rec)
                # 打印结果
    except Exception as e:
        print('Error in record,  exit(2)')
        print(e)
        connection.close()
        exit(2)

    connection.commit()
    connection.close()
    return (datalist)


if __name__ == '__main__':

    curr_stock = 'sz300750'
    xdate = '2018-11-21'
    print('Connecting to the database...' + DBuser + '@' + DBhost)
    daylist = xch_one_day(curr_stock, xdate)
    print(daylist)