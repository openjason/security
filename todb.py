#CREATE DATABASE stock character set utf8 collate utf8_bin;

'''
CREATE TABLE IF NOT EXISTS `sz300750` (
  `xdate` datetime DEFAULT NULL,
  `price` float DEFAULT NULL,
  `pdiff` float DEFAULT NULL,
  `volume` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `bors` char(8) CHARACTER SET latin1 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
'''

#grant all privileges on stock.* to jcc@'%' identified by 'password';
#flush privileges;
#LOAD DATA LOW_PRIORITY LOCAL INFILE 'F:\\dev\\GitHub\\security\\usz300750_1121.log' REPLACE INTO TABLE `stock`.`sz300750` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (`xdate`, `price`, `pdiff`, `volume`, `amount`, `bors`);

import pymysql.cursors



# Connect to the database
'''
connection = pymysql.connect(host='1.1.1.178',
                             user='jcc',
                             password='jccisme',
                             db='stock',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
'''
datalist = []
with open('sz300750_1122.log', 'r',encoding='UTF-8') as file_to_read:
    lines = file_to_read.readline()
    while True:
        lines = file_to_read.readline()  # 整行读取数据
        if not lines:
            break
            pass
        datalist.append(lines)
        pass
    pass
print(datalist)
quit()


try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()