#!/usr/bin/python3

import pymysql

#查询启用状态的数据源
class MysqlDB:

    def querystart(self):
        # 打开数据库连接
        db = pymysql.Connect(
            host='192.168.10.235',
            port=3306,
            user='root',
            passwd='123',
            db='console_data_crawler',
            charset='utf8mb4'
        )
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT do.id,s.scrapy_name,do.url FROM data_origin `do` ,script s WHERE do.`script_id` = s.id  AND do.`status` = 0 AND do.is_delete =0"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            # 关闭数据库连接

        except:
            print("Error: unable to fetch data")
        db.close()
        return results

