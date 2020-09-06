# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import datetime

import pymysql

from .items import ProductItem, CommentItem


class MysqlPipeline(object):
    def __init__(self, host, user, password, database, port, charset):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            port=crawler.settings.get('MYSQL_PORT'),
            charset=crawler.settings.get('MYSQL_CHARSET')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            charset=self.charset
        )
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        now = datetime.datetime.now()
        data['create_datetime'] = data['update_datetime'] = now

        # 从数据库中查询产品是否存在
        product_title = data['title'] if 'title' in data else data.pop('product_title')
        select_sql = f"SELECT id FROM {ProductItem.table} WHERE title='{product_title}'"
        self.cursor.execute(select_sql)
        product_id = self.cursor.fetchone()
        if product_id:
            product_id = product_id[0]

        if isinstance(item, ProductItem):
            # 产品去重
            if product_id:
                return item
        elif isinstance(item, CommentItem):
            if not product_id:
                return item

            # 评论去重
            comment = data['comment']
            select_sql = (f"SELECT id FROM {CommentItem.table} WHERE "
                          f"product_id='{product_id}' AND comment='{comment}'")
            self.cursor.execute(select_sql)
            comment_id = self.cursor.fetchone()
            if comment_id:
                return item

            # 评论需要记录产品在数据库中的 id
            data['product_id'] = product_id

        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f'INSERT INTO {item.table} ({keys}) VALUES ({values})'

        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
        except Exception as e:
            spider.logger.error(e)
            self.db.rollback()
        return item
