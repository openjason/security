'''
#docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pwd mariadb
# docker exec -it cid /bin/bash

#CREATE DATABASE stock character set utf8 collate utf8_bin;
CREATE TABLE `sz300750` (
	`xdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`price` FLOAT NULL DEFAULT NULL,
	`pdiff` FLOAT NULL DEFAULT NULL,
	`volume` FLOAT NULL DEFAULT NULL,
	`amount` FLOAT NULL DEFAULT NULL,
	`bors` CHAR(8) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_520_ci',
	PRIMARY KEY (`xdate`)
)
COLLATE='utf8mb4_unicode_520_ci'
ENGINE=InnoDB
;

#CREATE USER 'jcc'@'%' IDENTIFIED BY 'pwd123456';
#grant all privileges on stock.* to 'jcc'@'%' identified by 'pwd123456' with grant option;
#grant all privileges on stock.* to 'jcc'@'%'; #不明确 with grant option 有什么作用, 没有这参数,有时授权无效.
#flush privileges;
# #alter user 'jcc'@'%' identified with mysql_native_password by 'pwd123456'; #修改加密规则 

#MYSQL图像化工具(HeidiSQL)，连接本地MYSQL时，提示“cacheing_sha2_password”的错误信息。
# 在MYSQL 的版本问题上，MYSQL8版本以上，默认存储密码的方式修为:caching_sha2_password,而MYSQL8版本以下，默认存储密码的方式为：mysql_native_password.
# # ALTER USER'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; #更新一下用户的密码 
# FLUSH PRIVILEGES; #刷新权限
# 重置密码：alter user'root'@'localhost' identified by 'root';

#LOAD DATA LOW_PRIORITY LOCAL INFILE 'F:\\dev\\GitHub\\security\\usz300750_1121.log' REPLACE INTO TABLE `stock`.`sz300750` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (`xdate`, `price`, `pdiff`, `volume`, `amount`, `bors`);

清理异常数据：
1、price偏离股价平均价20%
2、成交差价大于平均价2%
3、时间重复

                                 charset='utf8mb4',

'''

import pymysql.cursors
#import string

DBhost='1.1.1.177'
#DBhost='192.168.18.101'
DBuser='jcc'
DBpassword='pwd123456'
DBname='stock'

def writetodb(data_filename):
    BSM_dict = {'卖盘':'S','买盘':'B','中性盘':'N'}
    print('Connecting to the database...'+DBuser+'@'+DBhost)
    connection = pymysql.connect(host=DBhost,
                                 user=DBuser,
                                 password=DBpassword,
                                 db=DBname,
                                 cursorclass=pymysql.cursors.DictCursor)
    datalist = []
    with open(data_filename, 'r',encoding='UTF-8') as file_to_read:
        print('Reading daily record...')
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass
            datalist.append(lines)
            pass
        pass

    datalist.sort()
    price_sum = 0.0
    for rec_index in range(len(datalist)):#合计记录中买入价，求平均值
        onelinedata = datalist[rec_index].split(';')
        price_sum = price_sum + float(onelinedata[1])
    price_average = price_sum/len(datalist)

    previous_data = ''
    for rec_index in range(len(datalist)):
        onelinedata = datalist[rec_index].split(';')
        if datalist[rec_index][:20] == previous_data[:20]:
            print('Info...Remove dup data: '+datalist[rec_index])
            datalist[rec_index] = 'removed'
            previous_data = datalist[rec_index]
            continue
        previous_data = datalist[rec_index]

        if (float(onelinedata[1]) < 0) or (float(onelinedata[1]) > (price_average * 1.2)):
            print('Info...Remove price error data: '+datalist[rec_index])
            datalist[rec_index] = 'removed'
            continue
        temp_str = onelinedata[2]
        try:
            if abs(float(onelinedata[2])) > 3.0:# 缺口大于3.0,3.0只作参考
                print('Info...pdiff->0: '+datalist[rec_index])
                datalist_temp = onelinedata[0] + ';'+ onelinedata[1] + ';0;' + onelinedata[3]  + ';'+ onelinedata[4]  + ';'+ onelinedata[5]
                datalist[rec_index] = datalist_temp
                continue
        except:
            if onelinedata[2] != '--':
                print('Info... pdiff float error: ' + datalist[rec_index])
            continue

    for rec_index in range(len(datalist)):
        one_line = datalist[rec_index]
        if one_line == 'removed':
            continue
        one_rec = one_line.split(';')
        rec_changed = False
        if one_rec[2] == '--':
            one_rec[2] = 0
            rec_changed = True

        try:
            with connection.cursor() as cursor:
                # Create a new record
                bsm_value = BSM_dict[one_rec[5].strip()]
                sql = "INSERT INTO `sz300750` (`xdate`, `price`, `pdiff`, `volume`, `amount`, `bors`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (one_rec[0], one_rec[1], one_rec[2], one_rec[3], one_rec[4].replace(',', ''), bsm_value))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            print(one_rec)

            # with connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
        except Exception as e:
            print('Error in record,  exit(2)' + str(one_rec))
            print(e)
            connection.close()
            exit(2)
    connection.commit()
    connection.close()
if __name__ == '__main__':

    curr_stock = 'sz300750'
    curr_date = '2018-07-18'
    curr_filename = curr_stock+'_'+curr_date[5:]+'.log'

    writetodb(curr_filename)