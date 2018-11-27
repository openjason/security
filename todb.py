'''
#CREATE DATABASE stock character set utf8 collate utf8_bin;
CREATE TABLE IF NOT EXISTS `sz300750` (
  `xdate` datetime DEFAULT NULL,
  `price` float DEFAULT NULL,
  `pdiff` float DEFAULT NULL,
  `volume` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `bors` char(8) CHARACTER SET latin1 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

#CREATE USER 'jcc'@'%' IDENTIFIED BY 'pwd123456';
#grant all privileges on stock.* to 'jcc'@'%';
#flush privileges;
# #alter user 'jcc'@'%' identified with mysql_native_password by 'pwd123456'; #修改加密规则 

#MYSQL图像化工具(HeidiSQL)，连接本地MYSQL时，提示“cacheing_sha2_password”的错误信息。
# 在MYSQL 的版本问题上，MYSQL8版本以上，默认存储密码的方式修为:caching_sha2_password,而MYSQL8版本以下，默认存储密码的方式为：mysql_native_password.
# # ALTER USER'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; #更新一下用户的密码 
# FLUSH PRIVILEGES; #刷新权限
# 重置密码：alter user'root'@'localhost' identified by 'root';

#LOAD DATA LOW_PRIORITY LOCAL INFILE 'F:\\dev\\GitHub\\security\\usz300750_1121.log' REPLACE INTO TABLE `stock`.`sz300750` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (`xdate`, `price`, `pdiff`, `volume`, `amount`, `bors`);
'''

import pymysql.cursors
#import string

def writetodb():
    BSM_dict = {'卖盘':'S','买盘':'B','中性盘':'N'}
    print('Connecting to the database...')
    connection = pymysql.connect(host='1.1.1.178',
                                 user='jcc',
                                 password='jccisme',
                                 db='stock',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    datalist = []
    with open('sz300750_1122.log', 'r',encoding='UTF-8') as file_to_read:
        print('Reading daily record...')
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass
            datalist.append(lines)
            pass
        pass

    for rec_index in range(len(datalist)):
        one_line = datalist[rec_index]
        one_rec = one_line.split(';')
        rec_changed = False
        if one_rec[2] == '--':
            one_rec[2] = 0
            rec_changed = True

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `sz300750` (`xdate`, `price`, `pdiff`, `volume`, `amount`, `bors`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (one_rec[0], one_rec[1], one_rec[2], one_rec[3], one_rec[4].replace(',', ''), BSM_dict[one_rec[5].strip()]))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            print(one_rec[0])

            # with connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
        except:
            print('Error in record ' + one_rec[0])
            connection.close()
    connection.commit()
    connection.close()
if __name__ == '__main__':
    writetodb()