import datetime

import scrapy

from smzdm.items import ProductItem, CommentItem


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['www.smzdm.com']
    # 手机产品 24 小时排行
    start_urls = ['https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/']

    def parse(self, response):
        """解析产品标题、链接"""
        data = scrapy.Selector(response=response)
        items_xpath = '//ul[@id="feed-main-list"]//h5[@class="feed-block-title"]/a'
        items = data.xpath(items_xpath)

        for item in items[:10]:
            try:
                title = item.xpath('./text()').extract_first()
                link = item.xpath('./@href').extract_first()

                product_item = ProductItem()
                product_item['title'] = title
                product_item['link'] = link

                yield product_item
                yield scrapy.Request(url=link, callback=self.parse_comments)
            except Exception as e:
                self.logger.exception(e)

    def parse_comments(self, response):
        """解析产品评论"""
        data = scrapy.Selector(response=response)
        title_xpath = '//h1[@class="title J_title"]/text()'
        items_xpath = '//div[@id="commentTabBlockNew"]//li[@class="comment_list"]'
        title = data.xpath(title_xpath).extract_first().strip()
        items = data.xpath(items_xpath)

        for item in items:
            try:
                username_xpath = './/span[@itemprop="author"]/text()'
                comment_xpath = ('.//div[@class="comment_conBox"]'
                                 '/div[@class="comment_conWrap"]'
                                 '//span[@itemprop="description"]//text()')
                comment_time_meta_xpath = './/div[@class="time"]/meta/@content'
                comment_time_xpath = './/div[@class="time"]/text()'

                username = item.xpath(username_xpath).extract_first()
                comment = item.xpath(comment_xpath).extract()
                comment = '，'.join(c.strip() for c in comment if c.strip())
                comment_time_meta = item.xpath(comment_time_meta_xpath).extract_first()
                comment_time = item.xpath(comment_time_xpath).extract_first()
                comment_datetime = self._convert_datetime(comment_time_meta, comment_time)

                comment_item = CommentItem()
                comment_item['username'] = username
                comment_item['comment'] = comment
                comment_item['comment_datetime'] = comment_datetime
                comment_item['product_title'] = title

                yield comment_item
            except Exception as e:
                self.logger.exception(e)

        # 翻页
        next_page = data.xpath('//li[@class="pagedown"]//a/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_comments)

    @staticmethod
    def _convert_datetime(comment_time_meta, comment_time):
        """日期转换"""
        fmt = '%Y-%m-%d %H:%M:%S'
        now = datetime.datetime.now()

        if '分钟前' in comment_time:
            minutes = datetime.timedelta(minutes=int(comment_time[:-3]))
            comment_datetime = (now - minutes).strftime(fmt)
        elif '小时前' in comment_time:
            hours = datetime.timedelta(hours=int(comment_time[:-3]))
            comment_datetime = (now - hours).strftime(fmt)
        else:
            comment_datetime = comment_time_meta + comment_time[5:] + ':00'

        return comment_datetime
