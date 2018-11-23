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

import csv
import MySQLdb
DB_HOST = '1.1.1.198'
mydb = MySQLdb.connect(host='DB_HOST',
    user='jcc',
    passwd='jccisme',
    db='stock')
cursor = mydb.cursor()

csv_data = csv.reader(file('students.csv'))
for row in csv_data:

    cursor.execute('INSERT INTO testcsv(names, \
          classes, mark )' \
          'VALUES("%s", "%s", "%s")',
          row)
#close the connection to the database.
cursor.close()
print ("Done")
