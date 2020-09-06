# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    """产品"""
    # 表名
    table = 'product'
    # 标题
    title = scrapy.Field()
    # 链接
    link = scrapy.Field()


class CommentItem(scrapy.Item):
    """评论"""
    # 表名
    table = 'product_comment'
    # 用户名
    username = scrapy.Field()
    # 评论内容
    comment = scrapy.Field()
    # 评论时间
    comment_datetime = scrapy.Field()
    # 产品标题
    product_title = scrapy.Field()
