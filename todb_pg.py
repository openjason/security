#!/usr/bin/python
'''
#docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pwd mariadb
# docker exec -it cid /bin/bash
 
CREATE TABLE public."000063mx" (
    xdate TIMESTAMP NOT NULL,
    price double precision,
    pdiff double precision,
    volume double precision,
    amount double precision,
    bors character(8) DEFAULT NULL::bpchar
);
 
清理异常数据：
1、price偏离股价平均价20%
2、成交差价大于平均价2%
3、时间重复
 
'''
import psycopg2
import logging
from conf import set_logging
 
 
 
def writetodb(data_filename,table_name):
    BSM_dict = {'卖盘':'S','买盘':'B','中性盘':'N'}
    #print('Connecting to the database...'+conf.DBuser+'@'+conf.DBhost)
    connection = psycopg2.connect(database="st", user="postgres", password="123456", host="192.168.7.76", port="5432")
    print("Opened database successfully")
     
    datalist = []
    print('data_filename,table_name: ')
    print(data_filename,table_name)
 
    with open(data_filename[:8]+'\\'+data_filename, 'r',encoding='gbk') as file_to_read:
        lines = file_to_read.readline()
        print('Pass the first line : ',lines)
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            lines = lines.strip()            
            if not lines:
                break
                pass
            datalist.append(lines)
            pass
        pass
 
    datalist.sort()
    price_sum = 0.0
    for rec_index in range(len(datalist)):#合计记录中买入价，求平均值
        onelinedata = datalist[rec_index].split('|')
        price_sum = price_sum + float(onelinedata[1])
    price_average = price_sum/len(datalist)
    print('price_average :',price_average)
 
    previous_data = ''
    for rec_index in range(len(datalist)):
        onelinedata = datalist[rec_index].split('|')
        #金额明显偏离的删除
        if (float(onelinedata[1]) < 0) or (float(onelinedata[1]) > (price_average * 1.2)):
            print('Info...Remove price 偏差 data: '+datalist[rec_index])
            datalist[rec_index] = 'removed'
            continue
        temp_str = onelinedata[2]
        #print('test11:',onelinedata)
        try:
            if abs(float(onelinedata[2])) > 3.0:# 缺口大于3.0,3.0只作参考
                #print('Info...pdiff->0: '+datalist[rec_index])
                #print('test11:',onelinedata)
                datalist_temp = onelinedata[0] + "|" + onelinedata[1] + "|0|" + onelinedata[3]  + "|" + onelinedata[4]  + "|"+ onelinedata[5]
                #print('old',datalist[rec_index])
                #print('new',datalist_temp)
                datalist[rec_index] = datalist_temp
                continue
        except:
            if onelinedata[2] != '--':
                pass
                #print('Info... pdiff float error: ' + datalist[rec_index])
            continue
        #删除时间重复的记录
        if datalist[rec_index][:20] == previous_data[:20]:
            print('Info...Remove dup data: '+datalist[rec_index])
            datalist[rec_index] = 'removed'
            previous_data = datalist[rec_index]
            continue
        previous_data = datalist[rec_index]
    datalist.sort()
    for rec_index in range(len(datalist)):
        one_line = datalist[rec_index]
        if one_line == 'removed':
            continue
        one_rec = one_line.split('|')
        rec_changed = False
        #print('rec_index,one_line: ',rec_index,one_line)
        if one_rec[2] == '--':
            one_rec[2] = 0
            rec_changed = True
 
        try:
            with connection.cursor() as cursor:
                # Create a new record
                #print(one_rec[5].strip())
                bsm_value = BSM_dict[one_rec[5].strip()]
                sql = 'INSERT INTO "'+str(table_name)+'" (xdate, price, pdiff, volume, amount, bors) VALUES (%s, %s, %s, %s, %s, %s)'
                xdate = data_filename[9:19]+" "+one_rec[0]
#                print('xdate',xdate)
                cursor.execute(sql, (xdate, one_rec[1], one_rec[2], one_rec[3], one_rec[4], bsm_value))
        except Exception as e:
            print('Error in record, exit(err): ' + str(one_rec))
            print(e)
            connection.close()
            exit(2)
    connection.commit()
    connection.close()
if __name__ == '__main__':
    set_logging()
    
    curr_stock = 'sz000063'
    curr_date = '2019-01-02'
    curr_filename = curr_stock+'_'+curr_date+'.log'
    curr_table_name = '000063mx'
    writetodb(curr_filename,curr_table_name)
    
