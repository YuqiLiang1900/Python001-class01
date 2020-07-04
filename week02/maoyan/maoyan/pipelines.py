# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import csv
import json
import pymysql
from .settings import *


class MaoyanCSVPipeline(object):
    # item: 从爬虫文件 maoyan.py 中 yield 的 item 数据
    def process_item(self, item, spider):
        title = item['title']
        genres = item['genres']
        release_date = item['release_date']
        link = item['link']

        with open('maoyan.csv', mode='a+', encoding='utf_8_sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                title, genres, release_date, link
            ])

        return item


class MaoyanJSONPipeline(object):
    def __init__(self):
        self.file = open('maoyan_info.json', 'a+')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()


class MaoyanSqlPipeline(object):
    def __init__(self):
        # 爬虫程序启动时，只执行一次，一般用于建立数据库连接
        self.connection = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = 'ruiying7709',
            database = 'geektime_python_train',
            charset = 'utf8mb4'
        )
        # 数据库游标，用于操作数据库
        self.cursor = self.connection.cursor()
        print('Successfully launched the connection with the database.')
        
    def process_item(self, item, spider):
        try:
            # 将信息写入数据库
            sql_command = '''INSERT INTO week02_maoyan_movie(title, genres, 
            release_date, link) VALUES (%s, %s, %s, %s);'''
            print(sql_command)
            self.cursor.execute(sql_command, (item['title'], item['genres'],
                item['release_date'], item['link']))

            # 提交信息
            self.connection.commit()
            print('Successfully inserted', self.cursor.rowcount, 'rows of data')

        except Exception as e:
            # 输出错误信息
            print(e)
            self.connection.rollback()
            print('The transcation is rolled back due to the exception error.')
        # 必须写，此函数返回值会交给下一个管道处理item数据
        return item

    def close_spider(self, spider):
        # 爬虫程序结束时，只执行一次，一般用于断开数据库连接
        self.cursor.close()
        self.connection.close()
        print('Successfully shut down the connection with the database')
